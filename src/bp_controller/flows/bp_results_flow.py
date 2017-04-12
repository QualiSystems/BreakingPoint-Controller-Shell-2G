from bp_controller.actions.test_results_actions import TestResultsActions
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow


class BPResultsFlow(BPFlow):
    def __init__(self, session_manager, logger):
        super(BPResultsFlow, self).__init__(session_manager, logger)

    def get_results(self, test_id):
        with self._session_context_manager as rest_service:
            statistics_actions = TestResultsActions(rest_service, self._logger)
            pdf_results = statistics_actions.get_result_file(test_id, "pdf")
            return pdf_results
