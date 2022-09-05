"""
Test StcControllerShell2GDriver.
"""
# pylint: disable=redefined-outer-name
from pathlib import Path
from typing import Iterable

import pytest
from _pytest.fixtures import SubRequest
from cloudshell.api.cloudshell_api import AttributeNameValue, CloudShellAPISession, InputNameValue
from cloudshell.shell.core.driver_context import ResourceCommandContext
from cloudshell.traffic.helpers import get_reservation_id, get_resources_from_reservation, set_family_attribute
from cloudshell.traffic.tg import BREAKINGPOINT_CHASSIS_MODEL, BREAKINGPOINT_CONTROLLER_MODEL
from shellfoundry_traffic.test_helpers import TgTestHelpers, create_session_from_config

from src.breakingpoint_driver import BreakingPointControllerDriver

CHASSIS_920 = "192.168.26.49:admin:DxTbqlSgAVPmrDLlHvJrsA=="
PORTS_920 = ["BP_920/Module3/Port1", "BP_920/Module3/Port2"]

server_properties = {"bp_920": {"server": CHASSIS_920, "ports": PORTS_920}}

ALIAS = "BreakingPoint Controller"


@pytest.fixture(params=["bp_920"])
def server(request: SubRequest) -> dict:
    """Yield BreakingPoint device under test parameters."""
    return server_properties[request.param]


@pytest.fixture(scope="session")
def session() -> CloudShellAPISession:
    """Yield session."""
    return create_session_from_config()


@pytest.fixture()
def test_helpers(session: CloudShellAPISession) -> Iterable[TgTestHelpers]:
    """Yield initialized TestHelpers object."""
    test_helpers = TgTestHelpers(session)
    test_helpers.create_reservation()
    yield test_helpers
    test_helpers.end_reservation()


@pytest.fixture()
def driver(test_helpers: TgTestHelpers, server: dict) -> Iterable[BreakingPointControllerDriver]:
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
def context_wo_ports(session: CloudShellAPISession, test_helpers: TgTestHelpers, server: dict) -> ResourceCommandContext:
    """Yield ResourceCommandContext for shell command testing."""
    address, user, password = server["server"].split(":")
    attributes = [
        AttributeNameValue(f"{BREAKINGPOINT_CONTROLLER_MODEL}.Address", address),
        AttributeNameValue(f"{BREAKINGPOINT_CONTROLLER_MODEL}.User", user),
        AttributeNameValue(f"{BREAKINGPOINT_CONTROLLER_MODEL}.Password", password),
        AttributeNameValue(f"{BREAKINGPOINT_CONTROLLER_MODEL}.Test Files Location", "C:\\Temp"),
    ]
    session.AddServiceToReservation(test_helpers.reservation_id, BREAKINGPOINT_CONTROLLER_MODEL, ALIAS, attributes)
    return test_helpers.resource_command_context(service_name=ALIAS)


@pytest.fixture()
def context(
    session: CloudShellAPISession, test_helpers: TgTestHelpers, context_wo_ports: ResourceCommandContext, server: dict
) -> ResourceCommandContext:
    """Yield ResourceCommandContext for shell command testing."""
    session.AddResourcesToReservation(test_helpers.reservation_id, [server["ports"][0].split("/")[0]], shared=True)
    session.AddResourcesToReservation(test_helpers.reservation_id, server["ports"])
    reservation_ports = get_resources_from_reservation(
        context_wo_ports, f"{BREAKINGPOINT_CHASSIS_MODEL}.GenericTrafficGeneratorPort"
    )
    set_family_attribute(context_wo_ports, reservation_ports[0].Name, "Logical Name", "interface 1")
    set_family_attribute(context_wo_ports, reservation_ports[1].Name, "Logical Name", "interface 2")
    return context_wo_ports


class TestBreakingPointControllerDriver:
    """Test direct driver calls."""

    def test_get_file(self, driver: BreakingPointControllerDriver, context: ResourceCommandContext) -> None:
        """Test load_config command."""
        output = driver.get_test_file(context, "BitBlaster")
        assert Path(output).exists()

    def test_load_config(self, driver: BreakingPointControllerDriver, context: ResourceCommandContext) -> None:
        """Test load_config command."""
        config_file = Path(__file__).parent.joinpath("TestConfig.bpt")
        driver.load_config(context, config_file.as_posix())


class TestBreakingPointControllerShell:
    """Test indirect Shell calls."""

    def test_get_file(self, session: CloudShellAPISession, context: ResourceCommandContext) -> None:
        """Test Load Configuration command."""
        cmd_inputs = [InputNameValue("test_name", "BitBlaster")]
        output = session.ExecuteCommand(get_reservation_id(context), ALIAS, "Service", "get_test_file", cmd_inputs)
        assert Path(output.Output).exists()

    def test_load_config(self, session: CloudShellAPISession, context: ResourceCommandContext) -> None:
        """Test Load Configuration command."""
        cmd_inputs = [InputNameValue("config_file_location", Path(__file__).parent.joinpath("TestConfig.bpt").as_posix())]
        session.ExecuteCommand(get_reservation_id(context), ALIAS, "Service", "load_config", cmd_inputs)
