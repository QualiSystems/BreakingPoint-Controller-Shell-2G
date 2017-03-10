import json
import re

from bp_controller.actions.test_network_actions import TestNetworkActions
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow
from cloudshell.tg.breaking_point.flows.exceptions import BPFlowException


class BPTestNetworkFlow(BPFlow):
    def get_interfaces(self, network_name):
        if network_name:
            with self._session_manager.get_session() as rest_service:
                test_network_actions = TestNetworkActions(rest_service, self._logger)
                network_info = test_network_actions.get_network_neighborhood(network_name)
            test_interfaces = {}
            for key, value in network_info.iteritems():
                interface_id = key.split(':')[1]
                result = re.search(r'number:\s*(?P<id>\d+)', value, re.IGNORECASE)
                if result:
                    number = result.group('id')
                    test_interfaces[int(number)] = str(interface_id).lower()
                else:
                    BPFlowException(self.__class__.__name__, 'Interface number is not defined')
            return test_interfaces
        else:
            raise BPFlowException(self.__class__.__name__, 'Network name cannot be empty')
