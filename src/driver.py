from bp_controller.runners.bp_load_configuration_runner import BPTestRunner
from cloudshell.networking.devices.driver_helper import get_logger_with_thread_id, get_api
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

class BreakingPointControllerDriver(ResourceDriverInterface):
    def __init__(self):
        pass

    def initialize(self, context):
        """
        :param context: ResourceCommandContext,ReservationContextDetailsobject with all Resource Attributes inside
        :type context:  context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        pass

    def get_inventory(self, context):
        """
        Return device structure with all standard attributes
        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        pass

    def load_config(self, context, config_file_path):
        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        runner = BPTestRunner(context, logger, api)
        return runner.load_configuration(config_file_path)

    def send_arp(self, context):
        """ Send ARP for all objects (ports, devices, streams)
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        pass

    def start_traffic(self, context, blocking):
        """
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        pass

    def stop_traffic(self, context):
        """
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        pass

    def get_statistics(self, context, view_name, output_type):
        pass

    def cleanup(self):
        pass

    def keep_alive(self, context, cancellation_context):
        pass
