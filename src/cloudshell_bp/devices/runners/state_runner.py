#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell_bp.devices.flows.cli_action_flows import RunCommandFlow
from cloudshell_bp.devices.networking_utils import command_logging
from cloudshell_bp.devices.runners.interfaces.state_runner_interface import StateOperationsInterface


class StateRunner(StateOperationsInterface):
    def __init__(self, logger, api, resource_config, cli_handler):
        self._logger = logger
        self._api = api
        self.resource_config = resource_config
        self._resource_name = self.resource_config.name
        self._cli_handler = cli_handler

    @property
    def cli_handler(self):
        """CLI Handler property
        :return: CLI handler
        """

        return self._cli_handler

    @command_logging
    def health_check(self):
        """Verify that device is accessible over CLI by sending ENTER for cli session"""

        api_response = "Online"

        result = "Health check on resource {}".format(self._resource_name)
        try:
            health_check_flow = RunCommandFlow(self.cli_handler, self._logger)
            health_check_flow.execute_flow()
            result += " passed."
        except Exception as e:
            self._logger.exception(e)
            api_response = "Error"
            result += " failed."

        try:
            self._api.SetResourceLiveStatus(self._resource_name, api_response, result)
        except Exception:
            self._logger.error("Cannot update {} resource status on portal".format(self._resource_name))

        return result

    def shutdown(self):
        """Shutdown device"""

        raise Exception(self.__class__.__name__, "Shutdown command isn't available for the current device")
