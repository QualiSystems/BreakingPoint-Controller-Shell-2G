"""
BreakingPoint controller shell driver.
"""
import time

from cloudshell.shell.core.driver_context import CancellationContext, InitCommandContext, ResourceCommandContext
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext

from cloudshell_bp.devices.driver_helper import get_api, get_logger_with_thread_id
from cloudshell_bp.devices.standards.traffic.controller.configuration_attributes_structure import (
    GenericTrafficControllerResource,
)
from cloudshell_bp.tg.breaking_point.entities.bp_session import BPSession
from cloudshell_bp.tg.breaking_point.helpers.quali_rest_api_helper import QualiAPIHelper
from cloudshell_bp.tg.breaking_point.runners.bp_test_runner import BPTestRunner


class BreakingPointControllerDriver(ResourceDriverInterface):
    """BreakingPoint controller shell driver."""

    SHELL_NAME = "BreakingPoint Controller Shell 2G"
    SUPPORTED_OS = ["BreakingPoint"]

    def __init__(self) -> None:
        """Init must be without arguments, it is created with reflection at run time."""
        self._bp_sessions: dict = {}

    def _session_runner(self, context: ResourceCommandContext) -> BPTestRunner:
        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        resource_config = GenericTrafficControllerResource.from_context(
            shell_name=self.SHELL_NAME, supported_os=self.SUPPORTED_OS, context=context
        )
        reservation_id = context.reservation.reservation_id
        bp_session = self._bp_sessions.get(reservation_id, None)
        if not bp_session:
            bp_session = BPSession(reservation_id)
            self._bp_sessions[reservation_id] = bp_session

        return BPTestRunner(resource_config, bp_session, logger, api)

    def load_config(self, context: ResourceCommandContext, config_file_location: str) -> None:
        """Reserve ports and load configuration.

        :param context:
        :param config_file_location: configuration file location
        """
        cs_session = CloudShellSessionContext(context).get_api()
        cs_session.EnqueueCommand(
            context.reservation.reservation_id, context.resource.name, targetType="Service", commandName="keep_alive"
        )
        return self._session_runner(context).load_configuration(config_file_location.replace('"', ""))

    def start_traffic(self, context: ResourceCommandContext, blocking: str) -> None:
        """Start traffic on all ports.

        :param context: the context the command runs on
        :param bool blocking: True - return after traffic finish to run, False - return immediately
        """
        return self._session_runner(context).start_traffic(blocking)

    def stop_traffic(self, context: ResourceCommandContext) -> None:
        """Stop traffic on all ports.

        :param context: the context the command runs on
        """
        return self._session_runner(context).stop_traffic()

    def get_statistics(self, context: ResourceCommandContext, view_name: str, output_type: str) -> str:
        """Get real time statistics as sandbox attachment.

        :param context:
        :param str view_name: requested view name
        :param str output_type: CSV or JSON
        """
        return self._session_runner(context).get_statistics(view_name, output_type)

    def get_results(self, context: ResourceCommandContext) -> str:
        """Attach result file to the reservation.

        :param context:
        """
        runner = self._session_runner(context)
        return runner.get_results(context.reservation.environment_name, QualiAPIHelper.from_context(context, runner.logger))

    def get_test_file(self, context: ResourceCommandContext, test_name: str) -> str:
        """Download test file configuration and put to the folder defined in Test Files Location attribute.

        :param context:
        :param test_name: Name of the test
        """
        return self._session_runner(context).get_test_file(test_name)

    def send_arp(self, context: ResourceCommandContext) -> None:
        """Send ARP/ND for all protocols.

        :param context:
        """

    def start_protocols(self, context: ResourceCommandContext) -> None:
        """Start all protocols.

        :param context:
        """

    def stop_protocols(self, context: ResourceCommandContext) -> None:
        """Stop all protocols.

        :param context:
        """

    def run_quick_test(self, context: ResourceCommandContext) -> None:
        """Run quick test (API only command).

        :param context:
        """

    def get_session_id(self, context: ResourceCommandContext) -> None:
        """Get REST session ID (API only command).

        :param context:
        """

    def get_children(self, context: ResourceCommandContext, obj_ref: str, child_type: str) -> None:
        """Get list of children (API only command).

        :param context:
        :param str obj_ref: valid object reference
        :param str child_type: requested children type. If None returns all children
        """

    def get_attributes(self, context: ResourceCommandContext, obj_ref: str) -> None:
        """Get object attributes (API only command).

        :param context:
        :param str obj_ref: valid object reference
        """

    def set_attribute(self, context: ResourceCommandContext, obj_ref: str, attr_name: str, attr_value: str) -> None:
        """Set traffic generator object attribute (API only command).

        :param context:
        :param str obj_ref: valid object reference
        :param str attr_name: attribute name
        :param str attr_value: attribute value
        """

    def cleanup_reservation(self, context) -> None:
        """Clear reservation when it ends.

        :param context:
        """
        reservation_id = context.reservation.reservation_id
        bp_session = self._bp_sessions.get(reservation_id, None)
        if bp_session:
            logger = get_logger_with_thread_id(context)
            api = get_api(context)
            resource_config = GenericTrafficControllerResource.from_context(
                shell_name=self.SHELL_NAME, supported_os=self.SUPPORTED_OS, context=context
            )
            test_runner = BPTestRunner(resource_config, bp_session, logger, api)
            test_runner.close_session()
            del self._bp_sessions[reservation_id]

    def initialize(self, context: InitCommandContext) -> None:
        """Initialize BreakingPoint controller shell (from API)."""

    def cleanup(self) -> None:
        """Cleanup BreakingPoint controller shell (from API)."""

    # pylint: disable=unused-argument
    def keep_alive(self, context: ResourceCommandContext, cancellation_context: CancellationContext) -> None:
        """Keep BreakingPoint controller shell sessions alive (from TG controller API)."""
        while not cancellation_context.is_cancelled:
            time.sleep(2)
        if cancellation_context.is_cancelled:
            self.cleanup()
