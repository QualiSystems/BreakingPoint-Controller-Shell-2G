from cloudshell_bp.tg.breaking_point.flows.bp_autoload_flow import BPAutoloadFlow
from cloudshell_bp.tg.breaking_point.rest_api.rest_session_manager import RestSessionContextManager
from cloudshell_bp.tg.breaking_point.runners.bp_runner import BPRunner


class BPAutoloadRunner(BPRunner):
    def __init__(self, resource_config, shell_name, api, logger):
        """
        :type resource_config cloudshell.devices.standards.traffic.chassis.configuration_attributes_structure.GenericTrafficChassisResource
        :param shell_name
        :param logger:
        :param api:
        """
        super(BPAutoloadRunner, self).__init__(api, logger)
        self._resource_config = resource_config
        self.shell_name = shell_name
        self.session_context_manager = self._init_session_manager()

    def _init_session_manager(self):
        bp_address = self._resource_config.address
        bp_username = self._resource_config.user
        bp_password = self.api.DecryptPassword(self._resource_config.password).Value
        return RestSessionContextManager(bp_address, bp_username, bp_password, self.logger)

    @property
    def _autoload_flow(self):
        return BPAutoloadFlow(self.session_context_manager, self.logger)

    def discover(self):
        return self._autoload_flow.autoload_details(self.shell_name)
