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
        Return device structure with all standard attributes
        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        return AutoLoadDetails([], [])

    def load_config(self, context, config_file_location):
        with self._runners_pool.actual_runner(context) as runner:
            return runner.load_configuration(config_file_location.replace('"', ''))

    def load_pcap(self, context, pcap_file_location):
        with self._runners_pool.actual_runner(context) as runner:
            return runner.load_pcap(pcap_file_location.replace('"', ''))

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
            return runner.get_statistics(view_name, output_type)

    def get_results(self, context):
        with self._runners_pool.actual_runner(context) as runner:
            return runner.get_results()

    def cleanup(self):
        self._runners_pool.close_all_runners()

    def keep_alive(self, context, cancellation_context):
        pass
        # logger = get_logger_with_thread_id(context)
        # logger.debug(context)
        # if hasattr(context, 'reservation'):
        #     logger.debug('KEEPALIVE_RESERVATION {}'.format(context.reservation.reservation_id))
        # while not cancellation_context.is_cancelled:
        #     time.sleep(1)

        # with self._runners_pool.actual_runner(context) as runner:
        #     return runner.close()
        # raise Exception(self.__class__.__name__, 'Keepalive canceled, {}'.format(context.reservation.reservation_id))
