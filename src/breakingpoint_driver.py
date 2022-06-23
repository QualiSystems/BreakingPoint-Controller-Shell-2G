import time

from cloudshell.shell.core.driver_context import CancellationContext, ResourceCommandContext
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

from cloudshell_bp.devices.driver_helper import get_api, get_logger_with_thread_id
from cloudshell_bp.devices.standards.traffic.controller.configuration_attributes_structure import (
    GenericTrafficControllerResource,
)
from cloudshell_bp.tg.breaking_point.entities.bp_session import BPSession
from cloudshell_bp.tg.breaking_point.helpers.quali_rest_api_helper import QualiAPIHelper
from cloudshell_bp.tg.breaking_point.runners.bp_test_runner import BPTestRunner


class BreakingPointControllerDriver(ResourceDriverInterface):
    SHELL_NAME = "BreakingPoint Controller Shell 2G"
    SUPPORTED_OS = ["BreakingPoint"]

    def __init__(self):
        """
        ctor must be without arguments, it is created with reflection at run time
        """
        self._bp_sessions = {}

    def _session_runner(self, context):
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

    def load_config(self, context, config_file_location):
        """Reserve ports and load configuration

        :param context:
        :param str config_file_location: configuration file location
        :return:
        """
        return self._session_runner(context).load_configuration(config_file_location.replace('"', ""))

    def start_traffic(self, context, blocking):
        """Start traffic on all ports

        :param context: the context the command runs on
        :param bool blocking: True - return after traffic finish to run, False - return immediately
        """
        return self._session_runner(context).start_traffic(blocking)

    def stop_traffic(self, context):
        """Stop traffic on all ports

        :param context: the context the command runs on
        """
        return self._session_runner(context).stop_traffic()

    def get_statistics(self, context, view_name, output_type):
        """Get real time statistics as sandbox attachment

        :param context:
        :param str view_name: requested view name
        :param str output_type: CSV or JSON
        :return:
        """
        return self._session_runner(context).get_statistics(view_name, output_type)

    def get_results(self, context):
        """
        Attach result file to the reservation
        :param context:
        :return:
        """
        runner = self._session_runner(context)
        return runner.get_results(context.reservation.environment_name, QualiAPIHelper.from_context(context, runner.logger))

    def get_test_file(self, context, test_name):
        """
        Download test file configuration and put to the folder defined in Test Files Location attribute
        :param context:
        :param test_name: Name of the test
        :return:
        """

        return self._session_runner(context).get_test_file(test_name)

    def send_arp(self, context):
        """Send ARP/ND for all protocols

        :param context:
        :return:
        """
        pass

    def start_protocols(self, context):
        """Start all protocols

        :param context:
        :return:
        """
        pass

    def stop_protocols(self, context):
        """Stop all protocols

        :param context:
        :return:
        """
        pass

    def run_quick_test(self, context):
        """Run quick test

        :param context:
        :return:
        """
        pass

    def get_session_id(self, context):
        """API only command to get REST session ID

        :param context:
        :return:
        """
        pass

    def get_children(self, context, obj_ref, child_type):
        """API only command to get list of children

        :param context:
        :param str obj_ref: valid object reference
        :param str child_type: requested children type. If None returns all children
        :return:
        """
        pass

    def get_attributes(self, context, obj_ref):
        """API only command to get object attributes

        :param context:
        :param str obj_ref: valid object reference
        :return:
        """
        pass

    def set_attribute(self, context, obj_ref, attr_name, attr_value):
        """API only command to set traffic generator object attribute

        :param context:
        :param str obj_ref: valid object reference
        :param str attr_name: attribute name
        :param str attr_value: attribute value
        :return:
        """
        pass

    def cleanup_reservation(self, context):
        """Clear reservation when it ends

        :param context:
        :return:
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

    def initialize(self, context):
        pass

    def cleanup(self):
        """
        :return:
        """
        pass

    def keep_alive(self, context: ResourceCommandContext, cancellation_context: CancellationContext) -> None:
        """Keep BreakingPoint controller shell sessions alive (from TG controller API)."""
        while not cancellation_context.is_cancelled:
            time.sleep(2)
        if cancellation_context.is_cancelled:
            self.cleanup()
