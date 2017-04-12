from bp_controller.actions.test_statistics_actions import TestStatisticsActions
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow


class BPStatisticsFlow(BPFlow):
    def get_rt_statistics(self, test_id, view_name):
        with self._session_context_manager as rest_service:
            statistics_actions = TestStatisticsActions(rest_service, self._logger)
            stats = statistics_actions.get_real_time_statistics(test_id, view_name)
            return stats
