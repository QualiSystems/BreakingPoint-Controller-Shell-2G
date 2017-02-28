from bp_controller.flows.bp_load_configuration_flow import BPLoadConfigurationFlow
from cloudshell.tg.breaking_point.runners.bp_runner import BPRunner


class BPTestRunner(BPRunner):
    @property
    def _load_configuration_flow(self):
        return BPLoadConfigurationFlow(self.session_manager, self.logger)

    def load_configuration(self, test_file_path):
        self._load_configuration_flow.load_configuration(test_file_path)
