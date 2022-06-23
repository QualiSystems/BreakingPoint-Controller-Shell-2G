from threading import Lock

from cloudshell_bp.tg.breaking_point.rest_actions.auth_actions import AuthActions
from cloudshell_bp.tg.breaking_point.rest_api.rest_json_client import RestJsonClient


class RestSessionContextManager(object):
    def __init__(self, hostname, username, password, logger):
        self.__lock = Lock()
        self._hostname = hostname
        self._username = username
        self._password = password
        self._logger = logger
        self.__session = None
        self.__auth_actions = None

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    @property
    def _session(self):
        if not self.__session:
            self.__session = RestJsonClient(self._hostname)
        return self.__session

    @property
    def _auth_actions(self):
        if not self.__auth_actions:
            self.__auth_actions = AuthActions(self._session, self._logger)
        return self.__auth_actions

    def _destroy_session(self):
        if self.__auth_actions:
            self.__auth_actions.logout()
            self.__session = None
            self.__auth_actions = None

    def __del__(self):
        self._destroy_session()

    def __enter__(self):
        """
        :return:
        :rtype: RestJsonClient
        """
        self.__lock.acquire()
        if not self._auth_actions.logged_in():
            try:
                self._auth_actions.login(self._username, self._password)
            except:
                self.__lock.release()
                raise
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__lock.release()

    def __eq__(self, other):
        """
        :param RestSessionContextManager other:
        :rtype: bool
        """
        return self._hostname == other._hostname and self._username == other._username and self._password == other._password
