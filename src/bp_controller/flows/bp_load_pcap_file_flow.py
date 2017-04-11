from bp_controller.actions.test_configuration_actions import TestConfigurationActions
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow


class BPLoadPcapFileFlow(BPFlow):
    def load_pcap(self, pcap_file_path):
        with self._session_context_manager as rest_service:
            configuration_actions = TestConfigurationActions(rest_service, self._logger)
            file_name = configuration_actions.import_pcap(pcap_file_path).get('result')
            return file_name

