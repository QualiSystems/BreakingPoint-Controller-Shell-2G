from abc import ABCMeta, abstractmethod


class StateOperationsInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def health_check(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass
