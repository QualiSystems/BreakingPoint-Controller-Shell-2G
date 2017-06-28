import time
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
        Autoload inventory
        Return device structure with all standard attributes
        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        return AutoLoadDetails([], [])

    def load_config(self, context, config_file_location):
        """
        Load configuration file and reserve ports
        :param context: 
        :param config_file_location: 
        :return: 
        """
        with self._runners_pool.actual_runner(context) as runner:
            return runner.load_configuration(config_file_location.replace('"', ''))

    # def load_pcap(self, context, pcap_file_location):
    #     with self._runners_pool.actual_runner(context) as runner:
    #         return runner.load_pcap(pcap_file_location.replace('"', ''))

    def start_traffic(self, context, blocking):
        """
        Start traffic
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        :param blocking:
        """
        with self._runners_pool.actual_runner(context) as runner:
            return runner.start_traffic(blocking)

    def stop_traffic(self, context):
        """
        Stop traffic and unreserving ports
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        with self._runners_pool.actual_runner(context) as runner:
            return runner.stop_traffic()

    def get_statistics(self, context, view_name, output_type):
        """
        Get real time statistics
        :param context: 
        :param view_name: 
        :param output_type: 
        :return: 
        """
        with self._runners_pool.actual_runner(context) as runner:
            return runner.get_statistics(view_name, output_type)

    def get_results(self, context):
        """
        Attach result file to the reservation
        :param context: 
        :return: 
        """
        with self._runners_pool.actual_runner(context) as runner:
            return runner.get_results()

    def get_test_file(self, context, test_name):
        """
        Download test file configuration and put to the folder defined in Test Files Location attribute
        :param context: 
        :param test_name: Name of the test
        :return: 
        """
        with self._runners_pool.actual_runner(context) as runner:
            return runner.get_test_file(test_name)

    def cleanup(self):
        """
        Close runners
        :return: 
        """
        self._runners_pool.close_all_runners()

    def keep_alive(self, context, cancellation_context):
        while not cancellation_context.is_cancelled:
            time.sleep(1)

        with self._runners_pool.actual_runner(context) as runner:
            return runner.close()
