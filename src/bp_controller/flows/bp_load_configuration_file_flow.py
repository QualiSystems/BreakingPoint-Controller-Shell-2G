from bp_controller.actions.test_configuration_actions import TestConfigurationActions
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow


class BPLoadConfigurationFileFlow(BPFlow):
    def load_configuration(self, test_file_path):
        with self._session_context_manager as rest_service:
            configuration_actions = TestConfigurationActions(rest_service, self._logger)
            test_name = configuration_actions.import_test(test_file_path).get('result')
            return test_name
