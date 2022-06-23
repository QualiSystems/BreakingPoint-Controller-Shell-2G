from abc import ABCMeta

from cloudshell_bp.tg.breaking_point.rest_api.rest_session_manager import RestSessionContextManager


class BPFlow(object):
    __metaclass__ = ABCMeta

    def __init__(self, session_context_manager, logger):
        """
        :param session_context_manager:
        :type session_context_manager: RestSessionContextManager
        :param logger:
        """
        self._session_context_manager = session_context_manager
        self._logger = logger
