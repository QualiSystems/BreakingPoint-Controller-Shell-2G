from bp_controller.actions.test_statistics_actions import TestStatisticsActions
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow
from cloudshell.tg.breaking_point.flows.exceptions import BPFlowException


class BPStatisticsFlow(BPFlow):
    def get_statistics(self, test_id, file_format):
        if not file_format or not file_format.lower() in ['csv', 'xml']:
            raise BPFlowException(self.__class__.__name__, 'Incorrect file format, supportde csv or json only')
        with self._session_manager.get_session() as rest_service:
            statistics_actions = TestStatisticsActions(rest_service, self._logger)
            stats = statistics_actions.get_result_file(test_id, file_format.lower())
            return stats

    def get_rt_statistics(self, test_id, view_name):
        with self._session_manager.get_session() as rest_service:
            statistics_actions = TestStatisticsActions(rest_service, self._logger)
            stats = statistics_actions.get_real_time_statistics(test_id, view_name)
            return stats
