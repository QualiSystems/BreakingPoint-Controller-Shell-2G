from abc import ABCMeta, abstractmethod


class FirmwareRunnerInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def load_firmware(self, path, vrf_management_name):
        pass
