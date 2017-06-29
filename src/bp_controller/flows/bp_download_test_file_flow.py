from bp_controller.actions.test_configuration_actions import TestConfigurationActions
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow


class BPDownloadTestFileFlow(BPFlow):
    def download_test_file(self, test_name):
        with self._session_context_manager as rest_service:
            configuration_actions = TestConfigurationActions(rest_service, self._logger)
            test_file_content = configuration_actions.export_test(test_name)
            return test_file_content
