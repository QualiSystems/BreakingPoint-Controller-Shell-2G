from abc import ABCMeta, abstractmethod


class ConnectivityOperationsInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def apply_connectivity_changes(self, request):
        pass
