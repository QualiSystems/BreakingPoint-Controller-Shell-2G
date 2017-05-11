import re

from mock import Mock, patch, PropertyMock
from unittest2 import TestCase

from bp_controller.runners.bp_test_runner import BPTestRunner
from cloudshell.tg.breaking_point.rest_api.rest_json_client import RestClientUnauthorizedException
from cloudshell.tg.breaking_point.runners.exceptions import BPRunnerException


class TestBPTestRunner(TestCase):
    def setUp(self):
        self._context = Mock()
        self._logger = Mock()
        self._api = Mock()
        self._instance = BPTestRunner(self._context, self._logger, self._api)

    def test_init(self):
        self.assertIsNone(self._instance._test_id)
        self.assertIsNone(self._instance._test_name)

    @patch('bp_controller.runners.bp_test_runner.BPRunner')
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._cs_reservation_details', new_callable=PropertyMock)
    def test_context_setter(self, cs_reservation_details_prop, bp_runner_class):
        new_value = Mock()
        cs_reservation_details = Mock()
        cs_reservation_details_prop.return_value = cs_reservation_details
        self._instance.context = new_value
        bp_runner_class.context.fset.assert_called_once_with(self._instance, new_value)
        self.assertIs(cs_reservation_details.context, new_value)

    @patch('bp_controller.runners.bp_test_runner.BPRunner')
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._cs_reservation_details', new_callable=PropertyMock)
    def test_logger_setter(self, cs_reservation_details_prop, bp_runner_class):
        new_value = Mock()
        cs_reservation_details = Mock()
        cs_reservation_details_prop.return_value = cs_reservation_details
        self._instance.logger = new_value
        bp_runner_class.logger.fset.assert_called_once_with(self._instance, new_value)
        self.assertIs(cs_reservation_details.logger, new_value)

    @patch('bp_controller.runners.bp_test_runner.BPRunner')
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._cs_reservation_details', new_callable=PropertyMock)
    def test_api_setter(self, cs_reservation_details_prop, bp_runner_class):
        new_value = Mock()
        cs_reservation_details = Mock()
        cs_reservation_details_prop.return_value = cs_reservation_details
        self._instance.api = new_value
        bp_runner_class.api.fset.assert_called_once_with(self._instance, new_value)
        self.assertIs(cs_reservation_details.api, new_value)

    @patch('bp_controller.runners.bp_test_runner.BPTestExecutionFlow')
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._session_context_manager', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner.logger', new_callable=PropertyMock)
    def test_test_execution_flow_getter(self, logger_prop, session_context_manager_prop, bp_test_execution_flow_class):
        logger = Mock()
        session_context_manager = Mock()
        logger_prop.return_value = logger
        session_context_manager_prop.return_value = session_context_manager
        bp_test_execution_flow_instance = Mock()
        bp_test_execution_flow_class.return_value = bp_test_execution_flow_instance
        self.assertIs(self._instance._test_execution_flow, bp_test_execution_flow_instance)
        self.assertIs(self._instance._test_execution_flow, bp_test_execution_flow_instance)
        bp_test_execution_flow_class.assert_called_once_with(session_context_manager, logger)

    @patch('bp_controller.runners.bp_test_runner.BPStatisticsFlow')
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._session_context_manager', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner.logger', new_callable=PropertyMock)
    def test_test_statistics_flow_getter(self, logger_prop, session_context_manager_prop, bp_flow_class):
        logger = Mock()
        session_context_manager = Mock()
        logger_prop.return_value = logger
        session_context_manager_prop.return_value = session_context_manager
        bp_flow_instance = Mock()
        bp_flow_class.return_value = bp_flow_instance
        self.assertIs(self._instance._test_statistics_flow, bp_flow_instance)
        self.assertIs(self._instance._test_statistics_flow, bp_flow_instance)
        bp_flow_class.assert_called_once_with(session_context_manager, logger)

    @patch('bp_controller.runners.bp_test_runner.BPResultsFlow')
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._session_context_manager', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner.logger', new_callable=PropertyMock)
    def test_test_results_flow_getter(self, logger_prop, session_context_manager_prop, bp_flow_class):
        logger = Mock()
        session_context_manager = Mock()
        logger_prop.return_value = logger
        session_context_manager_prop.return_value = session_context_manager
        bp_flow_instance = Mock()
        bp_flow_class.return_value = bp_flow_instance
        self.assertIs(self._instance._test_results_flow, bp_flow_instance)
        self.assertIs(self._instance._test_results_flow, bp_flow_instance)
        bp_flow_class.assert_called_once_with(session_context_manager, logger)

    @patch('bp_controller.runners.bp_test_runner.BPLoadConfigurationFileFlow')
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._session_context_manager', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner.logger', new_callable=PropertyMock)
    def test_test_configuration_file_flow_getter(self, logger_prop, session_context_manager_prop, bp_flow_class):
        logger = Mock()
        session_context_manager = Mock()
        logger_prop.return_value = logger
        session_context_manager_prop.return_value = session_context_manager
        bp_flow_instance = Mock()
        bp_flow_class.return_value = bp_flow_instance
        self.assertIs(self._instance._test_configuration_file_flow, bp_flow_instance)
        self.assertIs(self._instance._test_configuration_file_flow, bp_flow_instance)
        bp_flow_class.assert_called_once_with(session_context_manager, logger)

    @patch('bp_controller.runners.bp_test_runner.BPCSReservationDetails')
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner.context', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner.logger', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner.api', new_callable=PropertyMock)
    def test_cs_reservation_details_getter(self, api_prop, logger_prop, context_prop, bp_cs_reservation_details_class):
        logger = Mock()
        logger_prop.return_value = logger
        api = Mock()
        api_prop.return_value = api
        context = Mock()
        context_prop.return_value = context
        reservation_details = Mock()
        bp_cs_reservation_details_class.return_value = reservation_details
        self.assertIs(self._instance._cs_reservation_details, reservation_details)
        self.assertIs(self._instance._cs_reservation_details, reservation_details)
        bp_cs_reservation_details_class.assert_called_once_with(context, logger, api)

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._cs_reservation_details', new_callable=PropertyMock)
    def test_resource_address_getter(self, cs_reservation_details_prop):
        cs_reservation_details_inst = Mock()
        cs_reservation_details_prop.return_value = cs_reservation_details_inst
        resource_address = Mock()
        cs_reservation_details_inst.get_chassis_address.return_value = resource_address
        self.assertIs(self._instance._resource_address, resource_address)
        cs_reservation_details_inst.get_chassis_address.assert_called_once_with()

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._cs_reservation_details', new_callable=PropertyMock)
    def test_username_getter(self, cs_reservation_details_prop):
        cs_reservation_details_inst = Mock()
        cs_reservation_details_prop.return_value = cs_reservation_details_inst
        username = Mock()
        cs_reservation_details_inst.get_chassis_user.return_value = username
        self.assertIs(self._instance._username, username)
        cs_reservation_details_inst.get_chassis_user.assert_called_once_with()

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._cs_reservation_details', new_callable=PropertyMock)
    def test_password_getter(self, cs_reservation_details_prop):
        cs_reservation_details_inst = Mock()
        cs_reservation_details_prop.return_value = cs_reservation_details_inst
        password = Mock()
        cs_reservation_details_inst.get_chassis_password.return_value = password
        self.assertIs(self._instance._password, password)
        cs_reservation_details_inst.get_chassis_password.assert_called_once_with()

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._session_context_manager', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._cs_reservation_details', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner.logger', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.PortReservationHelper')
    def test_port_reservation_helper(self, port_reservation_helper_class, logger_prop, cs_reservation_details_prop,
                                     session_context_manager_prop):
        logger = Mock()
        logger_prop.return_value = logger
        session_context_manager = Mock()
        session_context_manager_prop.return_value = session_context_manager
        cs_reservation_details = Mock()
        cs_reservation_details_prop.return_value = cs_reservation_details
        port_reservation_helper = Mock()
        port_reservation_helper_class.return_value = port_reservation_helper
        self.assertIs(self._instance._port_reservation_helper, port_reservation_helper)
        self.assertIs(self._instance._port_reservation_helper, port_reservation_helper)
        port_reservation_helper_class.assert_called_once_with(session_context_manager, cs_reservation_details, logger)

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._test_configuration_file_flow', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._port_reservation_helper', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.ElementTree')
    def test_load_configuration(self, element_tree_class, port_reservation_helper_prop, configuration_file_flow_prop):
        port_reservation_helper = Mock()
        configuration_file_flow = Mock()
        port_reservation_helper_prop.return_value = port_reservation_helper
        configuration_file_flow_prop.return_value = configuration_file_flow
        test_name = Mock()
        configuration_file_flow.load_configuration.return_value = test_name
        parse_file_mock = Mock()
        find_mock = Mock()
        test_model = Mock()
        element_tree_class.parse.return_value = parse_file_mock
        parse_file_mock.getroot.return_value = find_mock
        find_mock.find.return_value = test_model
        network_name = Mock()
        test_model.get.return_value = network_name
        interface = Mock()
        test_model.findall.return_value = [interface]
        interface.get.return_value = '3'
        file_path = Mock()
        self._instance.load_configuration(file_path)
        configuration_file_flow.load_configuration.assert_called_once_with(file_path)
        self.assertIs(self._instance._test_name, test_name)
        element_tree_class.parse.assert_called_once_with(file_path)
        parse_file_mock.getroot.assert_called_once_with()
        find_mock.find.assert_called_once_with('testmodel')
        test_model.get.assert_called_once_with('network')
        test_model.findall.assert_called_once_with('interface')
        interface.get.assert_called_once_with('number')
        port_reservation_helper.reserve_ports.assert_called_once_with(network_name, [3])

    def test_start_traffic_empty_name(self):
        with self.assertRaisesRegex(BPRunnerException, 'Load configuration first'):
            self._instance.start_traffic(Mock())

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._port_reservation_helper', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._test_execution_flow', new_callable=PropertyMock)
    def test_start_traffic_not_blocking(self, test_execution_flow_prop, port_reservation_helper_prop):
        test_execution_flow = Mock()
        port_reservation_helper = Mock()
        test_execution_flow_prop.return_value = test_execution_flow
        port_reservation_helper_prop.return_value = port_reservation_helper
        test_name = Mock()
        self._instance._test_name = test_name
        test_id = Mock()
        test_execution_flow.start_traffic.return_value = test_id
        group_id = Mock()
        port_reservation_helper.group_id = group_id
        self._instance.start_traffic('False')
        self.assertIs(test_id, self._instance._test_id)
        test_execution_flow.start_traffic.assert_called_once_with(test_name, group_id)
        test_execution_flow.block_while_test_running.assert_not_called()
        port_reservation_helper.unreserve_ports.assert_not_called()

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._port_reservation_helper', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._test_execution_flow', new_callable=PropertyMock)
    def test_start_traffic_blocking(self, test_execution_flow_prop, port_reservation_helper_prop):
        test_execution_flow = Mock()
        port_reservation_helper = Mock()
        test_execution_flow_prop.return_value = test_execution_flow
        port_reservation_helper_prop.return_value = port_reservation_helper
        test_name = Mock()
        self._instance._test_name = test_name
        test_id = Mock()
        test_execution_flow.start_traffic.return_value = test_id
        group_id = Mock()
        port_reservation_helper.group_id = group_id
        self._instance.start_traffic('True')
        self.assertIs(test_id, self._instance._test_id)
        test_execution_flow.start_traffic.assert_called_once_with(test_name, group_id)
        test_execution_flow.block_while_test_running.assert_called_once_with(test_id)
        port_reservation_helper.unreserve_ports.assert_called_once_with()

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._port_reservation_helper', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._test_execution_flow', new_callable=PropertyMock)
    def test_start_traffic_unreserve_if_raises_exception(self, test_execution_flow_prop, port_reservation_helper_prop):
        test_execution_flow = Mock()
        port_reservation_helper = Mock()
        test_execution_flow_prop.return_value = test_execution_flow
        port_reservation_helper_prop.return_value = port_reservation_helper
        test_name = Mock()
        self._instance._test_name = test_name
        test_execution_flow.start_traffic.side_effect = Exception()
        group_id = Mock()
        port_reservation_helper.group_id = group_id
        with self.assertRaises(Exception):
            self._instance.start_traffic('False')
        port_reservation_helper.unreserve_ports.assert_called_once_with()

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._port_reservation_helper', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._test_execution_flow', new_callable=PropertyMock)
    def test_start_traffic_unreserve_if_raises_exception(self, test_execution_flow_prop, port_reservation_helper_prop):
        test_execution_flow = Mock()
        port_reservation_helper = Mock()
        test_execution_flow_prop.return_value = test_execution_flow
        port_reservation_helper_prop.return_value = port_reservation_helper
        test_name = Mock()
        self._instance._test_name = test_name
        test_execution_flow.start_traffic.side_effect = RestClientUnauthorizedException()
        group_id = Mock()
        port_reservation_helper.group_id = group_id
        with self.assertRaises(RestClientUnauthorizedException):
            self._instance.start_traffic('False')
        port_reservation_helper.unreserve_ports.assert_not_called()

    def stop_traffic_raise_exception(self):
        with self.assertRaisesRegex(BPRunnerException, 'Test id is not defined'):
            self._instance.stop_traffic()

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._port_reservation_helper', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._test_execution_flow', new_callable=PropertyMock)
    def test_stop_traffic(self, test_execution_flow_prop, port_reservation_helper_prop):
        test_execution_flow = Mock()
        port_reservation_helper = Mock()
        test_execution_flow_prop.return_value = test_execution_flow
        port_reservation_helper_prop.return_value = port_reservation_helper
        test_id = Mock()
        test_name = Mock()
        self._instance._test_id = test_id
        self._instance._test_name = test_name
        self._instance.stop_traffic()
        test_execution_flow.stop_traffic.assert_called_once_with(test_id)
        port_reservation_helper.unreserve_ports.assert_called_once_with()
        self.assertIsNone(self._instance._test_name)

    def test_get_statistics_raises_exception(self):
        with self.assertRaisesRegex(BPRunnerException, 'Test id is not defined'):
            self._instance.get_statistics(Mock(), Mock())

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._test_statistics_flow', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.json')
    def test_get_statistics_json(self, json, test_statistics_flow_prop):
        test_statistics_flow = Mock()
        result = Mock()
        test_statistics_flow_prop.return_value = test_statistics_flow
        test_statistics_flow.get_rt_statistics.return_value = result
        statistics = Mock()
        json.dumps.return_value = statistics
        view_name = Mock()
        test_id = Mock()
        self._instance._test_id = test_id
        self.assertIs(self._instance.get_statistics(view_name, 'JSON'), statistics)
        test_statistics_flow.get_rt_statistics.assert_called_once_with(test_id, view_name)
        json.dumps.assert_called_once_with(result, indent=4, sort_keys=True, ensure_ascii=False)

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._test_statistics_flow', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.io')
    @patch('bp_controller.runners.bp_test_runner.csv')
    def test_get_statistics_csv(self, csv, io, test_statistics_flow_prop):
        test_statistics_flow = Mock()
        result = Mock()
        test_statistics_flow_prop.return_value = test_statistics_flow
        test_statistics_flow.get_rt_statistics.return_value = result
        statistics = Mock()
        view_name = Mock()
        test_id = Mock()
        output = Mock()
        io.BytesIO.return_value = output

        w = Mock()
        csv.DictWriter.return_value = w
        keys = Mock()
        result.keys.return_value = keys
        getvalue_strip_mock = Mock()
        getvalue_strip_mock.strip.return_value = statistics
        output.getvalue.return_value = getvalue_strip_mock
        self._instance._test_id = test_id
        self.assertIs(self._instance.get_statistics(view_name, 'CSV'), statistics)
        test_statistics_flow.get_rt_statistics.assert_called_once_with(test_id, view_name)
        io.BytesIO.assert_called_once_with()
        csv.DictWriter.assert_called_once_with(output, keys)
        w.writeheader.assert_called_once_with()
        w.writerow.assert_called_once_with(result)
        output.getvalue.assert_called_once_with()
        getvalue_strip_mock.strip.assert_called_once_with('\r\n')

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._test_statistics_flow', new_callable=PropertyMock)
    def test_get_statistics_incorrect_format(self, test_statistics_flow_prop):
        test_statistics_flow = Mock()
        result = Mock()
        test_statistics_flow_prop.return_value = test_statistics_flow
        test_statistics_flow.get_rt_statistics.return_value = result
        view_name = Mock()
        test_id = Mock()
        self._instance._test_id = test_id
        with self.assertRaisesRegex(BPRunnerException, 'Incorrect file format'):
            self._instance.get_statistics(view_name, 'Incorrect')
        test_statistics_flow.get_rt_statistics.assert_called_once_with(test_id, view_name)

    def test_get_results_not_test_id(self):
        with self.assertRaisesRegex(BPRunnerException, 'Test id is not defined'):
            self._instance.get_results()

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._test_results_flow', new_callable=PropertyMock)
    @patch('bp_controller.runners.bp_test_runner.create_quali_api_instance')
    def test_get_results_flow(self, create_quali_api_instance, test_results_flow_prop):
        quali_api = Mock()
        create_quali_api_instance.return_value = quali_api
        test_results_flow = Mock()
        test_results_flow_prop.return_value = test_results_flow
        test_id = 'test_id'
        env_name = 'env_name'
        result = Mock()
        test_results_flow.get_results.return_value = result
        self._instance._test_id = test_id
        self._context.reservation.environment_name = env_name
        self._instance.get_results()
        test_results_flow.get_results.assert_called_once_with(test_id)
        create_quali_api_instance.assert_called_once_with(self._context, self._logger)
        quali_api.login.assert_called_once_with()
        env_name = re.sub("\s+", "_", env_name)
        test_id = re.sub("\s+", "_", test_id)
        file_name = "{0}_{1}.pdf".format(env_name, test_id)
        quali_api.upload_file.assert_called_once_with(self._context.reservation.reservation_id, file_name=file_name,
                                                      file_stream=result)

    @patch('bp_controller.runners.bp_test_runner.BPTestRunner._port_reservation_helper', new_callable=PropertyMock)
    def test_close(self, port_reservation_helper_prop):
        self._context.reservation.reservation_id = 'test'
        port_reservation_helper_prop.unreserve_ports.assewrt_called_once_with()
