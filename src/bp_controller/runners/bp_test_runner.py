import csv
import json
from bp_controller.helpers.port_reservation_helper import PortReservationHelper
import re

import io
from xml.etree import ElementTree

from bp_controller.flows.bp_load_configuration_file_flow import BPLoadConfigurationFileFlow
from bp_controller.flows.bp_load_pcap_file_flow import BPLoadPcapFileFlow
from bp_controller.flows.bp_results_flow import BPResultsFlow
from bp_controller.flows.bp_statistics_flow import BPStatisticsFlow
from bp_controller.flows.bp_test_execution_flow import BPTestExecutionFlow
from bp_controller.helpers.bp_cs_reservation_details import BPCSReservationDetails
from bp_controller.helpers.quali_rest_api_helper import QualiAPIHelper
from cloudshell.tg.breaking_point.runners.bp_runner import BPRunner
from cloudshell.tg.breaking_point.runners.exceptions import BPRunnerException


class BPTestRunner(BPRunner):
    def __init__(self, context, logger, api):
        """
        Test runner, hold current configuration fo specific test
        :param context:
        :param logger:
        :param api:
        """
        super(BPTestRunner, self).__init__(context, logger, api)
        self._test_id = None
        self._test_name = None

        self.__test_execution_flow = None
        self.__test_statistics_flow = None
        self.__test_results_flow = None
        self.__reservation_details = None
        self.__port_reservation_helper = None

    @property
    def _test_execution_flow(self):
        """
        :return:
        :rtype: BPTestExecutionFlow
        """
        if not self.__test_execution_flow:
            self.__test_execution_flow = BPTestExecutionFlow(self._session_manager, self.logger)
        return self.__test_execution_flow

    @property
    def _test_statistics_flow(self):
        """
        :return:
        :rtype: BPStatisticsFlow
        """
        if not self.__test_statistics_flow:
            self.__test_statistics_flow = BPStatisticsFlow(self._session_manager, self.logger)
        return self.__test_statistics_flow

    @property
    def _test_results_flow(self):
        """
        :return:
        :rtype: BPStatisticsFlow
        """
        if not self.__test_results_flow:
            self.__test_results_flow = BPResultsFlow(self._session_manager, self.logger)
        return self.__test_results_flow

    @property
    def _cs_reservation_details(self):
        """
        :return:
        :rtype: BPReservationDetails
        """
        if not self.__reservation_details:
            self.__reservation_details = BPCSReservationDetails(self.context, self.logger, self.api)
        else:
            self.__reservation_details.api = self.api
            self.__reservation_details.context = self.context
            self.__reservation_details.logger = self.logger
        return self.__reservation_details

    @property
    def _port_reservation_helper(self):
        """
        :return:
        :rtype: PortReservationHelper
        """
        if not self.__port_reservation_helper:
            self.__port_reservation_helper = PortReservationHelper(self._session_manager, self._cs_reservation_details,
                                                                   self.logger)
        return self.__port_reservation_helper

    def load_configuration(self, file_path):
        self._test_name = BPLoadConfigurationFileFlow(self._session_manager,
                                                      self.logger).load_configuration(file_path)
        test_model = ElementTree.parse(file_path).getroot().find('testmodel')
        network_name = test_model.get('network')
        interfaces = []
        for interface in test_model.findall('interface'):
            interfaces.append(int(interface.get('number')))
        self._port_reservation_helper.reserve_ports(network_name, interfaces)

    def load_pcap(self, file_path):
        response_file_name = BPLoadPcapFileFlow(self._session_manager, self.logger).load_pcap(file_path)
        self.logger.info("Response received: " + str(response_file_name))
        file_name = file_path.split("\\")[-1].split(".")[0]
        if not re.search(response_file_name, file_name, re.IGNORECASE):
            raise BPRunnerException(self.__class__.__name__, 'Unable to load pcap file')

    def start_traffic(self, blocking):
        if not self._test_name:
            raise BPRunnerException(self.__class__.__name__, 'Load configuration first')
        try:
            self._test_id = self._test_execution_flow.start_traffic(self._test_name,
                                                                    self._port_reservation_helper.group_id)
            if blocking.lower() == 'true':
                self._test_execution_flow.block_while_test_running(self._test_id)
                self._port_reservation_helper.unreserve_ports()
        except:
            self._port_reservation_helper.unreserve_ports()
            raise

    def stop_traffic(self):
        if not self._test_id:
            raise BPRunnerException(self.__class__.__name__, 'Test id is not defined, run the test first')
        self._test_execution_flow.stop_traffic(self._test_id)
        self._port_reservation_helper.unreserve_ports()

    def get_statistics(self, view_name, output_format):
        if not self._test_id:
            raise BPRunnerException(self.__class__.__name__, 'Test id is not defined, run the test first')
        result = self._test_statistics_flow.get_rt_statistics(self._test_id, view_name)
        if output_format.lower() == 'json':
            statistics = json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False)
            # print statistics
            # self.api.WriteMessageToReservationOutput(self.context.reservation.reservation_id, statistics)
        elif output_format.lower() == 'csv':
            output = io.BytesIO()
            w = csv.DictWriter(output, result.keys())
            w.writeheader()
            w.writerow(result)
            statistics = output.getvalue().strip('\r\n')

            # self.api.WriteMessageToReservationOutput(self.context.reservation.reservation_id,
            #                                          output.getvalue().strip('\r\n'))
        else:
            raise BPRunnerException(self.__class__.__name__, 'Incorrect file format, supported csv or json only')
        return statistics

    def get_results(self):
        if not self._test_id:
            raise BPRunnerException(self.__class__.__name__, 'Test id is not defined, run the test first')
        pdf_result = self._test_results_flow.get_results(self._test_id)
        domain = "Global"
        if hasattr(self.context, 'reservation') and self.context.reservation:
            domain = self.context.reservation.domain

        if hasattr(self.context, 'remote_reservation') and self.context.remote_reservation:
            domain = self.context.remote_reservation.domain

        quali_api_helper = QualiAPIHelper(self.logger, self.context.connectivity.server_address, domain)
        quali_api_helper.login(self.context.connectivity.admin_auth_token)
        env_name = re.sub("\s+", "_", self.context.reservation.environment_name)
        test_id = re.sub("\s+", "_", self._test_id)
        file_name = "{0}_{1}.pdf".format(env_name, test_id)
        save_file_name = "D:\\tests\\reports\\{0}.pdf".format(self.context.reservation.reservation_id)
        quali_api_helper.upload_file(self.context.reservation.reservation_id, file_name=file_name,
                                     file_stream=pdf_result)
        with open(save_file_name, 'w') as result_file:
            result_file.write(pdf_result)

        return "Please check attachments for results"

    def close(self):
        reservation_id = self.context.reservation.reservation_id
        self.logger.debug('Close session for reservation ID: '.format(reservation_id))
        self._port_reservation_helper.unreserve_ports()
