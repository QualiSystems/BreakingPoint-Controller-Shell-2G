from xml.etree import ElementTree
from bp_controller.actions.port_reservation_actions import PortReservationActions
from bp_controller.actions.test_configuration_actions import TestConfigurationActions
from bp_controller.actions.test_execution_actions import TestExecutionActions
from bp_controller.actions.test_statistics_actions import TestStatisticsActions
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow


class BPStatisticsFlow(BPFlow):
    def get_statistics(self, test_id, format):
        with self._session_manager.get_session() as rest_service:
            statistics_actions = TestStatisticsActions(rest_service, self._logger)
            stats = statistics_actions.get_result_file(test_id, 'pdf')
            return stats

    def _get_test_info(self, file_path):
        test_info = {}
        root = ElementTree.parse(file_path).getroot()
        testmodel = root.find('testmodel')
        test_info['name'] = testmodel.get('name')
        test_info['network'] = testmodel.get('network')
        test_info['ports'] = testmodel.findall('interface')
        return test_info
