import time

from bp_controller.flows.bp_load_configuration_file_flow import BPLoadConfigurationFileFlow
from bp_controller.flows.bp_port_reservation_flow import BPPortReservationFlow
from bp_controller.flows.bp_statistics_flow import BPStatisticsFlow
from bp_controller.flows.bp_test_execution_flow import BPTestExecutionFlow
from bp_controller.flows.bp_test_network_flow import BPTestNetworkFlow
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
        self.__test_statistics_flow = None
        self.reservation_info = reservation_info
        self._test_id = None
        self._test_name = None
        self._network_name = None
        self.__test_execution_flow = None
        self._group_id = None

    @property
    def _test_execution_flow(self):
        """
        :return:
        :rtype: BPTestExecutionFlow
        """
        if not self.__test_execution_flow:
            self.__test_execution_flow = BPTestExecutionFlow(self.session_manager, self.logger)
        return self.__test_execution_flow

    @property
    def _test_statistics_flow(self):
        """
        :return:
        :rtype: BPStatisticsFlow
        """
        if not self.__test_statistics_flow:
            self.__test_statistics_flow = BPStatisticsFlow(self.session_manager, self.logger)
        return self.__test_statistics_flow

    def load_configuration(self, file_path):
        self._load_test_file(file_path)
        self._reserve_ports()

    def _load_test_file(self, test_file_path):
        self._test_name, self._network_name = BPLoadConfigurationFileFlow(self.session_manager,
                                                                          self.logger).load_configuration(
            test_file_path)

    def _reserve_ports(self):
        cs_reserved_ports = BPReservationDetails(self.context, self.logger, self.api).get_chassis_ports()
        bp_test_interfaces = BPTestNetworkFlow(self.session_manager, self.logger).get_interfaces(self._network_name)
        reservation_order = []
        for bp_interface in bp_test_interfaces.values():
            if bp_interface in cs_reserved_ports:
                reservation_order.append(cs_reserved_ports[bp_interface])

        reservation_flow = BPPortReservationFlow(self.session_manager, self.logger)
        self._group_id = self.reservation_info.reserve(self.context.reservation.reservation_id, reservation_order)
        reservation_flow.reserve_ports(self._group_id, reservation_order)

    def start_traffic(self, blocking):
        self._test_id = self._test_execution_flow.start_traffic(self._test_name, self._group_id)
        if blocking:
            while self._test_execution_flow.test_rinning(self._test_id):
                time.sleep(5)

    def stop_traffic(self):
        return self._test_execution_flow.stop_traffic(self._test_id)

    def get_statistics(self, output_format):
        return self._test_statistics_flow.get_statistics(self._test_id, output_format)
