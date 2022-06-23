from cloudshell_bp.devices.autoload.autoload_builder import AutoloadDetailsBuilder
from cloudshell_bp.tg.breaking_point.actions.autoload_actions import AutoloadActions
from cloudshell_bp.tg.breaking_point.autoload.bp_autoload import BPAutoload
from cloudshell_bp.tg.breaking_point.flows.bp_flow import BPFlow


class BPAutoloadFlow(BPFlow):
    def autoload_details(self, shell_name):
        with self._session_context_manager as session:
            autoload_actions = AutoloadActions(session, self._logger)
            ports_info = autoload_actions.get_ports_info()
            bp_autoload = BPAutoload(ports_info, self._logger)
            autoload_builder = AutoloadDetailsBuilder(bp_autoload.collect_details(shell_name))
            return autoload_builder.autoload_details()
