from abc import ABCMeta, abstractmethod


class AutoloadOperationsInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def discover(self):
        pass
