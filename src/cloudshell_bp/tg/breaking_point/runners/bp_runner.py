from abc import ABCMeta


class BPRunner(object):
    __metaclass__ = ABCMeta

    def __init__(self, api, logger):
        """
        :param logging.Logger logger:
        :param cloudshell.api.cloudshell_api.CloudShellAPISession api:
        """
        self._api = api
        self._logger = logger

    @property
    def logger(self):
        return self._logger

    @property
    def api(self):
        return self._api
