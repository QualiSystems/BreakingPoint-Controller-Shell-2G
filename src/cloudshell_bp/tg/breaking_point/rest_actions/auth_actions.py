from cloudshell_bp.tg.breaking_point.rest_actions.rest_actions import RestActions
from cloudshell_bp.tg.breaking_point.rest_api.rest_json_client import (
    RestClientException,
    RestClientUnauthorizedException,
    RestJsonClient,
)


class AuthActions(RestActions):
    def login(self, username, password):
        """
        Login request
        :param username:
        :param password:
        :return:
        """
        self._logger.debug("Login request with  Username: {0}, Password: {1}".format(username, password))
        uri = "/api/v1/auth/session"
        json_data = {"username": username, "password": password}
        self._rest_service.request_post(uri, json_data)

    def logout(self):
        """
        Logout request
        :return:
        """
        self._logger.debug("Logout request")
        uri = "/api/v1/auth/session"
        try:
            self._rest_service.request_delete(uri)
        except RestClientException:
            pass

    def logged_in(self):
        """
        Check if logged-in
        :return:
        """
        self._logger.debug("Check logged-in request")
        uri = "/api/v1/bps/"
        logged_in = False
        try:
            self._rest_service.request_get(uri)
            logged_in = True
        except RestClientUnauthorizedException:
            pass
        return logged_in
