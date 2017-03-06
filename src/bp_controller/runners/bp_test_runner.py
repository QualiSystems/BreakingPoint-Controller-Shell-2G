from bp_controller.flows.bp_load_configuration_flow import BPLoadConfigurationFlow
from bp_controller.helpers.bp_reservation_details import BPReservationDetails
from cloudshell.tg.breaking_point.runners.bp_runner import BPRunner


class BPTestRunner(BPRunner):
    def __init__(self, context, logger, api, reservation_info):
        """
        Test runner, hold current configuration fo specific test
        :param context:
        :param logger:
        :param api:
        :param reservation_info:
        """
        super(BPTestRunner, self).__init__(context, logger, api)
        self.reservation_info = reservation_info
        self._test_id = None
        self._test_name = None
        self._network_name = None

        return

    def load_configuration(self, test_file_path):
        BPLoadConfigurationFlow(self.session_manager, self.logger)
        self._test_name, self._network_name = BPLoadConfigurationFlow(self.session_manager, self.logger).load_configuration(test_file_path)
        self._reserve_ports()

    def _reserve_ports(self):
        reservation_details = BPReservationDetails(self.context, self.logger, self.api)
        return reservation_details.get_chassis_ports()

    def start_traffic(self, blocking):
        pass

    def stop_traffic(self):
        pass

    def get_statistics(self, output_format):
        pass
