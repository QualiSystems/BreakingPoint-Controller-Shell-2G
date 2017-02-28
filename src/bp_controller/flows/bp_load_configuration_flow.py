from xml.etree import ElementTree
from bp_controller.actions.port_reservation_actions import PortReservationActions
from bp_controller.actions.test_configuration_actions import TestConfigurationActions
from bp_controller.actions.test_execution_actions import TestExecutionActions
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow


class BPLoadConfigurationFlow(BPFlow):
    def load_configuration(self, test_file_path):
        # test_name = re.sub(r'\.xml|\.bpt', '', basename(test_file_path))
        # test_file = open(test_file_path, 'rb')

        with self._session_manager.get_session() as rest_service:
            test_file_actions = TestConfigurationActions(rest_service, self._logger)
            test_name = test_file_actions.import_test(test_file_path).get('result')

            test_info = self._get_test_info(test_file_path)
            port_reservation = PortReservationActions(rest_service, self._logger)
            network_info = test_file_actions.get_network_neighborhood(test_info.get('network'))
            port_reservation.reserve_port(2, [0])

            # port_reservation.reserve_port(2,1)
            test_execution_actions = TestExecutionActions(rest_service, self._logger)
            result = test_execution_actions.start_test(test_info.get('name'))
            rts = test_execution_actions.get_real_time_statistics(result.get('testid'))
            tttt = test_execution_actions.running_tests()
            
            # while test_execution_actions.running_tests().get('sdsd'):
            #     time.sleep(1)
            test_execution_actions.stop_test(result.get('testid'))
            stats = test_execution_actions.get_results(result.get('testid'))

            print(test_name)

    def _get_test_info(self, file_path):
        test_info = {}
        root = ElementTree.parse(file_path).getroot()
        testmodel = root.find('testmodel')
        test_info['name'] = testmodel.get('name')
        test_info['network'] = testmodel.get('network')
        test_info['ports'] = testmodel.findall('interface')
        return test_info
