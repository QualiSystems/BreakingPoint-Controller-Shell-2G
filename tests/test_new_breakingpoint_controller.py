"""
Test StcControllerShell2GDriver.
"""
# pylint: disable=redefined-outer-name
import json
import os
import time
from pathlib import Path
from typing import Iterable

import pytest
from _pytest.fixtures import SubRequest
from cloudshell.api.cloudshell_api import AttributeNameValue, CloudShellAPISession, InputNameValue
from cloudshell.shell.core.driver_context import ResourceCommandContext
from cloudshell.traffic.helpers import get_reservation_id, get_resources_from_reservation, set_family_attribute
from cloudshell.traffic.tg import BREAKINGPOINT_CHASSIS_MODEL, BREAKINGPOINT_CONTROLLER_MODEL
from shellfoundry_traffic.test_helpers import TestHelpers, create_session_from_config

from new_src.breakingpoint_driver import BreakingPointControllerDriver

CHASSIS_920 = "192.168.26.72:admin:DxTbqlSgAVPmrDLlHvJrsA=="
PORTS_920 = ["BP_920/Module1/Port1", "BP_920/Module1/Port2"]

server_properties = {"bp_920": {"server": CHASSIS_920, "ports": PORTS_920}}

ALIAS = "BreakingPoint Controller"


@pytest.fixture(params=["bp_920"])
def server(request: SubRequest) -> dict:
    """Yield BreakingPoint device under test parameters."""
    return server_properties[request.param]


@pytest.fixture(scope="session")
def session() -> CloudShellAPISession:
    """Yield session."""
    yield create_session_from_config()


@pytest.fixture()
def test_helpers(session: CloudShellAPISession) -> Iterable[TestHelpers]:
    """Yield initialized TestHelpers object."""
    test_helpers = TestHelpers(session)
    test_helpers.create_reservation()
    yield test_helpers
    test_helpers.end_reservation()


@pytest.fixture()
def driver(test_helpers: TestHelpers, server: dict) -> Iterable[BreakingPointControllerDriver]:
    """Yield initialized BreakingPointControllerDriver."""
    address, user, password = server["server"].split(":")
    attributes = {
        f"{BREAKINGPOINT_CONTROLLER_MODEL}.Address": address,
        f"{BREAKINGPOINT_CONTROLLER_MODEL}.User": user,
        f"{BREAKINGPOINT_CONTROLLER_MODEL}.Password": password,
    }
    init_context = test_helpers.service_init_command_context(BREAKINGPOINT_CONTROLLER_MODEL, attributes)
    driver = BreakingPointControllerDriver()
    driver.initialize(init_context)
    yield driver
    driver.cleanup()


@pytest.fixture()
def context_wo_ports(session: CloudShellAPISession, test_helpers: TestHelpers, server: list) -> ResourceCommandContext:
    """Yield ResourceCommandContext for shell command testing."""
    address, user, password = server["server"].split(":")
    attributes = [
        AttributeNameValue(f"{BREAKINGPOINT_CONTROLLER_MODEL}.Address", address),
        AttributeNameValue(f"{BREAKINGPOINT_CONTROLLER_MODEL}.User", user),
        AttributeNameValue(f"{BREAKINGPOINT_CONTROLLER_MODEL}.Password", password),
    ]
    session.AddServiceToReservation(test_helpers.reservation_id, BREAKINGPOINT_CONTROLLER_MODEL, ALIAS, attributes)
    return test_helpers.resource_command_context(service_name=ALIAS)


@pytest.fixture()
def context(
    session: CloudShellAPISession, test_helpers: TestHelpers, context_wo_ports: ResourceCommandContext, server: list
) -> ResourceCommandContext:
    """Yield ResourceCommandContext for shell command testing."""
    session.AddResourcesToReservation(test_helpers.reservation_id, server["ports"])
    reservation_ports = get_resources_from_reservation(
        context_wo_ports, f"{BREAKINGPOINT_CHASSIS_MODEL}.GenericTrafficGeneratorPort"
    )
    set_family_attribute(context_wo_ports, reservation_ports[0].Name, "Logical Name", "interface 1")
    set_family_attribute(context_wo_ports, reservation_ports[1].Name, "Logical Name", "interface 2")
    return context_wo_ports


@pytest.fixture
def skip_if_offline(server: list) -> None:
    """Skip test on offline ports."""
    if [p for p in server[2] if "offline-debug" in p]:
        pytest.skip("offline-debug port")


class TestBreakingPointControllerDriver:
    """Test direct driver calls."""

    def test_load_config(self, driver: BreakingPointControllerDriver, context: ResourceCommandContext) -> None:
        """Test load_config command."""
        config_file = Path(__file__).parent.joinpath("TestConfig.bpt")
        driver.load_config(context, config_file.as_posix())

    @pytest.mark.usefixtures("skip_if_offline")
    def test_run_traffic(self, driver: BreakingPointControllerDriver, context: ResourceCommandContext) -> None:
        """Test traffic commands."""
        config_file = Path(__file__).parent.joinpath("test_config.tcc")
        driver.load_config(context, config_file)
        driver.send_arp(context)
        driver.start_traffic(context, "False")
        driver.stop_traffic(context)
        stats = driver.get_statistics(context, "generatorportresults", "JSON")
        assert int(stats["Port 1"]["TotalFrameCount"]) <= 4000
        driver.start_traffic(context, "True")
        time.sleep(2)
        stats = driver.get_statistics(context, "generatorportresults", "JSON")
        assert int(stats["Port 1"]["TotalFrameCount"]) >= 4000
        driver.get_statistics(context, "generatorportresults", "csv")

    @pytest.mark.usefixtures("skip_if_offline")
    def test_run_sequencer(self, driver: BreakingPointControllerDriver, context: ResourceCommandContext) -> None:
        """Test sequencer commands."""
        config_file = Path(__file__).parent.joinpath("test_sequencer.tcc")
        driver.load_config(context, config_file)
        driver.run_quick_test(context, "Start")
        driver.run_quick_test(context, "Wait")


class TestBreakingPointControllerShell:
    """Test indirect Shell calls."""

    @staticmethod
    def test_shell(session: CloudShellAPISession, context_wo_ports: ResourceCommandContext) -> None:
        """Test that the shell is up and running. This test does not require chassis or configuration."""
        session_id = session.ExecuteCommand(get_reservation_id(context_wo_ports), ALIAS, "Service", "get_session_id")
        assert os.environ["COMPUTERNAME"].replace("-", "_") in session_id.Output
        cmd_inputs = [
            InputNameValue("obj_ref", "system1"),
            InputNameValue("child_type", "project"),
        ]
        project = session.ExecuteCommand(get_reservation_id(context_wo_ports), ALIAS, "Service", "get_children", cmd_inputs)
        assert len(json.loads(project.Output)) == 1
        assert json.loads(project.Output)[0] == "project1"

    def test_load_config(self, session: CloudShellAPISession, context: ResourceCommandContext) -> None:
        """Test Load Configuration command."""
        self._load_config(session, context, Path(__file__).parent.joinpath("test_config.tcc"))

    @pytest.mark.usefixtures("skip_if_offline")
    def test_run_traffic(self, session: CloudShellAPISession, context: ResourceCommandContext) -> None:
        """Test traffic commands."""
        self._load_config(session, context, Path(__file__).parent.joinpath("test_config.tcc"))
        session.ExecuteCommand(get_reservation_id(context), ALIAS, "Service", "send_arp")
        session.ExecuteCommand(get_reservation_id(context), ALIAS, "Service", "start_protocols")
        cmd_inputs = [InputNameValue("blocking", "True")]
        session.ExecuteCommand(get_reservation_id(context), ALIAS, "Service", "start_traffic", cmd_inputs)
        time.sleep(2)
        cmd_inputs = [
            InputNameValue("view_name", "generatorportresults"),
            InputNameValue("output_type", "JSON"),
        ]
        stats = session.ExecuteCommand(get_reservation_id(context), ALIAS, "Service", "get_statistics", cmd_inputs)
        assert int(json.loads(stats.Output)["Port 1"]["TotalFrameCount"]) >= 4000

    @pytest.mark.usefixtures("skip_if_offline")
    def test_run_sequencer(self, session: CloudShellAPISession, context: ResourceCommandContext) -> None:
        """Test sequencer commands."""
        self._load_config(session, context, Path(__file__).parent.joinpath("test_sequencer.tcc"))
        cmd_inputs = [InputNameValue("command", "Start")]
        session.ExecuteCommand(get_reservation_id(context), ALIAS, "Service", "run_quick_test", cmd_inputs)
        cmd_inputs = [InputNameValue("command", "Wait")]
        session.ExecuteCommand(get_reservation_id(context), ALIAS, "Service", "run_quick_test", cmd_inputs)
        time.sleep(2)
        cmd_inputs = [
            InputNameValue("view_name", "generatorportresults"),
            InputNameValue("output_type", "JSON"),
        ]
        stats = session.ExecuteCommand(get_reservation_id(context), ALIAS, "Service", "get_statistics", cmd_inputs)
        assert int(json.loads(stats.Output)["Port 1"]["GeneratorIpv4FrameCount"]) == 8000

    @staticmethod
    def _load_config(session: CloudShellAPISession, context: ResourceCommandContext, config: Path) -> None:
        reservation_ports = get_resources_from_reservation(context, "STC Chassis Shell 2G.GenericTrafficGeneratorPort")
        set_family_attribute(context, reservation_ports[0].Name, "Logical Name", "Port 1")
        set_family_attribute(context, reservation_ports[1].Name, "Logical Name", "Port 2")
        cmd_inputs = [InputNameValue("config_file_location", config.as_posix())]
        session.ExecuteCommand(get_reservation_id(context), ALIAS, "Service", "load_config", cmd_inputs)
