from bp_controller.runners.bp_runner_pool import BPRunnersPool
from cloudshell.shell.core.driver_context import AutoLoadDetails
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface


class BreakingPointControllerDriver(ResourceDriverInterface):
    def __init__(self):
        self._runners_pool = BPRunnersPool()

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
        return AutoLoadDetails([], [])

    def load_config(self, context, config_file_location):
        with self._runners_pool.actual_runner(context) as runner:
            return runner.load_configuration(config_file_location)

    # def send_arp(self, context):
    #     """ Send ARP for all objects (ports, devices, streams)
    #     :param context: the context the command runs on
    #     :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
    #     """
    #     pass

    def start_traffic(self, context, blocking):
        """
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        :param blocking:
        """
        with self._runners_pool.actual_runner(context) as runner:
            return runner.start_traffic(blocking)

    def stop_traffic(self, context):
        """
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        with self._runners_pool.actual_runner(context) as runner:
            return runner.stop_traffic()

    def get_statistics(self, context, view_name, output_type):
        with self._runners_pool.actual_runner(context) as runner:
            return runner.get_statistics(output_type)

    def cleanup(self):
        pass

    def keep_alive(self, context, cancellation_context):
        pass
