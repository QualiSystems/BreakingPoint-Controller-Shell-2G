from cloudshell_bp.tg.breaking_point.actions.test_results_actions import TestResultsActions
from cloudshell_bp.tg.breaking_point.flows.bp_flow import BPFlow


class BPResultsFlow(BPFlow):
    def get_results(self, test_id):
        with self._session_context_manager as rest_service:
            statistics_actions = TestResultsActions(rest_service, self._logger)
            pdf_results = statistics_actions.get_result_file(test_id, "pdf")
            return pdf_results
