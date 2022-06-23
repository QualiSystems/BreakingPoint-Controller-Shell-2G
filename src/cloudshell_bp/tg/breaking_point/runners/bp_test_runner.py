import csv
import io
import json
import os
import re
from xml.etree import ElementTree

from cloudshell_bp.tg.breaking_point.flows.bp_download_test_file_flow import BPDownloadTestFileFlow
from cloudshell_bp.tg.breaking_point.flows.bp_load_configuration_file_flow import BPLoadConfigurationFileFlow
from cloudshell_bp.tg.breaking_point.flows.bp_load_pcap_file_flow import BPLoadPcapFileFlow
from cloudshell_bp.tg.breaking_point.flows.bp_port_reservation_flow import BPPortReservationFlow
from cloudshell_bp.tg.breaking_point.flows.bp_results_flow import BPResultsFlow
from cloudshell_bp.tg.breaking_point.flows.bp_statistics_flow import BPStatisticsFlow
from cloudshell_bp.tg.breaking_point.flows.bp_test_execution_flow import BPTestExecutionFlow
from cloudshell_bp.tg.breaking_point.helpers.bp_cs_reservation_details import BPCSReservationDetails
from cloudshell_bp.tg.breaking_point.helpers.port_reservation_helper import PortReservationHelper
from cloudshell_bp.tg.breaking_point.rest_api.rest_session_manager import RestSessionContextManager
from cloudshell_bp.tg.breaking_point.runners.bp_runner import BPRunner
from cloudshell_bp.tg.breaking_point.runners.exceptions import BPRunnerException


class BPTestRunner(BPRunner):
    def __init__(self, resource_config, bp_session, logger, api):
        """
        Test runner, hold current configuration fo specific test
        :type resource_config: cloudshell_bp.devices.standards.traffic.controller.configuration_attributes_structure.
        :type bp_session: cloudshell.tg.breaking_point.entities.bp_session.BPSession
        """
        super(BPTestRunner, self).__init__(api, logger)
        self._resource_config = resource_config
        self._bp_session = bp_session
        self.reservation_id = self._bp_session.cs_reservation_id

        self.__session_context_manager = None
        self.__test_execution_flow = None
        self.__test_statistics_flow = None
        self.__test_results_flow = None
        self.__test_configuration_file_flow = None
        self.__download_test_file_flow = None
        self.__reservation_details = None
        self.__port_reservation_flow = None
        self.__port_reservation_helper = None

    def _init_session_manager(self):
        bp_address = self._cs_reservation_details.get_chassis_address()
        bp_username = self._cs_reservation_details.get_chassis_user()
        bp_password = self._cs_reservation_details.get_chassis_password()
        return RestSessionContextManager(bp_address, bp_username, bp_password, self.logger)

    @property
    def session_context_manager(self):
        if not self.__session_context_manager:
            self.__session_context_manager = self._init_session_manager()
        return self.__session_context_manager

    @property
    def _cs_reservation_details(self):
        """
        :rtype: BPCSReservationDetails
        """
        if not self.__reservation_details:
            self.__reservation_details = BPCSReservationDetails(self.reservation_id, self.logger, self.api)
        return self.__reservation_details

    @property
    def _test_execution_flow(self):
        """
        :return:
        :rtype: BPTestExecutionFlow
        """
        if not self.__test_execution_flow:
            self.__test_execution_flow = BPTestExecutionFlow(self.session_context_manager, self.logger)
        return self.__test_execution_flow

    @property
    def _test_statistics_flow(self):
        """
        :return:
        :rtype: BPStatisticsFlow
        """
        if not self.__test_statistics_flow:
            self.__test_statistics_flow = BPStatisticsFlow(self.session_context_manager, self.logger)
        return self.__test_statistics_flow

    @property
    def _test_results_flow(self):
        """
        :return:
        :rtype: BPResultsFlow
        """
        if not self.__test_results_flow:
            self.__test_results_flow = BPResultsFlow(self.session_context_manager, self.logger)
        return self.__test_results_flow

    @property
    def _test_configuration_file_flow(self):
        if not self.__test_configuration_file_flow:
            self.__test_configuration_file_flow = BPLoadConfigurationFileFlow(self.session_context_manager, self.logger)
        return self.__test_configuration_file_flow

    @property
    def _download_test_file_flow(self):
        if not self.__download_test_file_flow:
            self.__download_test_file_flow = BPDownloadTestFileFlow(self.session_context_manager, self.logger)
        return self.__download_test_file_flow

    @property
    def _port_reservation_flow(self):
        if not self.__port_reservation_flow:
            self.__port_reservation_flow = BPPortReservationFlow(self.session_context_manager, self.logger)
        return self.__port_reservation_flow

    @property
    def _port_reservation_helper(self):
        """
        Port reservation operations
        :return:
        :rtype: PortReservationHelper
        """
        if not self.__port_reservation_helper:
            self.__port_reservation_helper = PortReservationHelper(
                self._port_reservation_flow, self._cs_reservation_details, self.logger
            )
        return self.__port_reservation_helper

    def _get_existing_path(self, file_path):
        """
        Looking for existing path
        :return:
        :rtype: basestring
        """
        test_files_location = self._resource_config.test_files_location
        search_order = [
            os.path.join(test_files_location or "", file_path),
            os.path.join(test_files_location or "", self.reservation_id, file_path),
            file_path,
        ]
        for path in search_order:
            if os.path.exists(path):
                return path
        raise BPRunnerException(
            self.__class__.__name__,
            'File {} does not exists or "Test Files Location" attribute was not specified'.format(file_path),
        )

    def load_configuration(self, file_path):
        """
        Upload configuration file and reserve ports
        :param file_path:
        :return:
        """
        file_path = self._get_existing_path(file_path)

        self._bp_session.test_name = self._test_configuration_file_flow.load_configuration(file_path)
        test_model = ElementTree.parse(file_path).getroot().find("testmodel")
        network_name = test_model.get("network")
        interfaces = []
        for interface in test_model.findall("interface"):
            interfaces.append(int(interface.get("number")))
        self._port_reservation_helper.reserve_ports(network_name, interfaces, self._bp_session)

    def load_pcap(self, file_path):
        response_file_name = BPLoadPcapFileFlow(self.session_context_manager, self.logger).load_pcap(file_path)
        self.logger.debug("Response received: " + str(response_file_name))
        file_name = file_path.split("\\")[-1].split(".")[0]
        if not re.search(response_file_name, file_name, re.IGNORECASE):
            raise BPRunnerException(self.__class__.__name__, "Unable to load pcap file")

    def start_traffic(self, blocking):
        """
        Start traffic
        :param blocking:
        :return:
        """
        if not self._bp_session.test_name:
            raise BPRunnerException(self.__class__.__name__, "Load configuration first")
        self._bp_session.test_id = self._test_execution_flow.start_traffic(
            self._bp_session.test_name, self._bp_session.reservation_group
        )
        if blocking.lower() == "true":
            self._test_execution_flow.block_while_test_running(self._bp_session.test_id)

    def stop_traffic(self):
        """
        Stop traffic
        :return:
        """
        if not self._bp_session.test_id:
            raise BPRunnerException(self.__class__.__name__, "Test id is not defined, run the test first")
        self._test_execution_flow.stop_traffic(self._bp_session.test_id)

    def get_statistics(self, view_name, output_format):
        """
        Real time statistics
        :param view_name:
        :param output_format:
        :return:
        """
        if not self._bp_session.test_id:
            raise BPRunnerException(self.__class__.__name__, "Test id is not defined, run the test first")
        result = self._test_statistics_flow.get_rt_statistics(self._bp_session.test_id, view_name)
        if output_format.lower() == "json":
            statistics = json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False)
            # print statistics
            # self.api.WriteMessageToReservationOutput(self.context.reservation.reservation_id, statistics)
        elif output_format.lower() == "csv":
            output = io.BytesIO()
            w = csv.DictWriter(output, result.keys())
            w.writeheader()
            w.writerow(result)
            statistics = output.getvalue().strip("\r\n")

            # self.api.WriteMessageToReservationOutput(self.context.reservation.reservation_id,
            #                                          output.getvalue().strip('\r\n'))
        else:
            raise BPRunnerException(self.__class__.__name__, "Incorrect file format, supported csv or json only")
        return statistics

    def get_results(self, environment_name, quali_api_helper):
        """
        Get test result file and attache it to the reservation
        :param str environment_name:
        :type quali_api_helper: cloudshell.tg.breaking_point.helpers.quali_rest_api_helper.QualiAPIHelper
        """
        if not self._bp_session.test_id:
            raise BPRunnerException(self.__class__.__name__, "Test id is not defined, run the test first")
        pdf_result = self._test_results_flow.get_results(self._bp_session.test_id)
        quali_api_helper.login()
        env_name = re.sub("\s+", "_", environment_name)
        test_id = re.sub("\s+", "_", self._bp_session.test_id)
        file_name = "{0}_{1}.pdf".format(env_name, test_id)
        quali_api_helper.upload_file(self.reservation_id, file_name=file_name, file_stream=pdf_result)
        return "Please check attachments for results"

    def get_test_file(self, test_name):
        """
        Download test file from BP
        :param test_name:
        :return:
        """
        test_files_location = self._resource_config.test_files_location

        if not test_files_location:
            raise BPRunnerException(self.__class__.__name__, "Test Files Location attribute is not defined")
        if not os.path.exists(test_files_location) or os.access(test_files_location, os.W_OK) is not True:
            raise BPRunnerException(
                self.__class__.__name__,
                'The location of the test files "{}" does not exist or is not writable'.format(test_files_location),
            )
        reservation_files = os.path.join(test_files_location, self.reservation_id)
        if not os.path.exists(reservation_files):
            os.makedirs(reservation_files)
        test_file_path = os.path.join(
            reservation_files,
            test_name + ".bpt",
        )
        test_file_content = self._download_test_file_flow.download_test_file(test_name)
        with open(test_file_path, "w") as f:
            f.write(test_file_content)
        return test_file_path

    def close_session(self):
        """
        Destroy
        :return:
        """
        reservation_id = self.reservation_id
        self.logger.debug("Close session for reservation ID: ".format(reservation_id))
        self._port_reservation_helper.unreserve_ports(self._bp_session)
