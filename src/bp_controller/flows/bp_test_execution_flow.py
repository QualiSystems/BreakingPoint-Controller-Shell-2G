import time

from bp_controller.actions.test_execution_actions import TestExecutionActions
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow


class BPTestExecutionFlow(BPFlow):
    def start_traffic(self, test_name, group_id):
        with self._session_context_manager as rest_service:
            test_execution_actions = TestExecutionActions(rest_service, self._logger)
            test_id = test_execution_actions.start_test(test_name, group_id)
            return test_id

    def stop_traffic(self, test_id):
        with self._session_context_manager as rest_service:
            test_execution_actions = TestExecutionActions(rest_service, self._logger)
            status = test_execution_actions.stop_test(test_id)
            return status.get('result')

    def block_while_test_running(self, test_id):
        with self._session_context_manager as rest_service:
            test_execution_actions = TestExecutionActions(rest_service, self._logger)
            running = True
            while running:
                self._logger.debug('Test {} is running'.format(test_id))
                status = test_execution_actions.get_test_status(test_id)
                running = 'incomplete' in status
                time.sleep(2)
