from bp_controller.flows.bp_load_configuration_flow import BPLoadConfigurationFlow
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

    @property
    def _load_configuration_flow(self):
        return BPLoadConfigurationFlow(self.session_manager, self.logger)

    def load_configuration_file(self, test_file_path):
        self._test_name = self._load_configuration_flow.load_configuration(test_file_path)

    def _reserve_ports(self):
        pass

    def start_traffic(self, blocking):
        pass

    def stop_traffic(self):
        pass

    def get_statistics(self, output_format):
        pass
