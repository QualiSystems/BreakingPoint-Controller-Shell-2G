from abc import ABCMeta, abstractmethod


class NetworkingResourceDriverInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def ApplyConnectivityChanges(self, context, request):
        pass

    @abstractmethod
    def run_custom_command(self, context, custom_command):
        pass

    @abstractmethod
    def run_custom_config_command(self, context, custom_command):
        pass

    @abstractmethod
    def save(self, context, folder_path, configuration_type, vrf_management_name):
        pass

    @abstractmethod
    def restore(self, context, path, configuration_type, restore_method, vrf_management_name):
        pass

    @abstractmethod
    def get_inventory(self, context):
        pass

    @abstractmethod
    def orchestration_restore(self, context, saved_artifact_info, custom_params):
        pass

    @abstractmethod
    def orchestration_save(self, context, mode, custom_params):
        pass

    @abstractmethod
    def health_check(self, context):
        pass

    @abstractmethod
    def load_firmware(self, context, path, vrf_management_name):
        pass

    @abstractmethod
    def shutdown(self, context):
        pass
