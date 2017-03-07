from xml.etree import ElementTree
from bp_controller.actions.test_configuration_actions import TestConfigurationActions
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow


class BPLoadConfigurationFileFlow(BPFlow):
    def load_configuration(self, test_file_path):
        with self._session_manager.get_session() as rest_service:
            configuration_actions = TestConfigurationActions(rest_service, self._logger)
            test_name = configuration_actions.import_test(test_file_path).get('result')
            network_name = ElementTree.parse(test_file_path).getroot().find('testmodel').get('network')
            return test_name, network_name
