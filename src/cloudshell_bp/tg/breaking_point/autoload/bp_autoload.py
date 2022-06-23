import re

from cloudshell_bp.devices.standards.traffic.chassis.autoload_structure import (
    GenericTrafficGeneratorModule,
    GenericTrafficGeneratorPort,
    TrafficGeneratorChassis,
)


class BPAutoload(object):
    PORT_PREFIX = "PORT"
    MOD_PREFIX = "MOD"

    def __init__(self, ports_info, logger):
        """
        :param logger:
        :return:
        """
        self.ports_info = ports_info
        self._logger = logger

    def collect_details(self, shell_name):
        root_resource = TrafficGeneratorChassis(shell_name, "Chassis 1", "CHASS0")
        modules = {}

        self._logger.debug("Collecting ports info")
        data = re.findall(r"\[slot=(\d+),port=(\d+)\]", self.ports_info)
        for mod_id, port_id in data:
            mod_unique_id = self.MOD_PREFIX + str(mod_id)
            port_unique_id = mod_unique_id + self.PORT_PREFIX + str(port_id)
            if mod_unique_id not in modules:
                module = GenericTrafficGeneratorModule(shell_name, "Module {}".format(mod_id), mod_unique_id)
                modules[mod_unique_id] = module
                root_resource.add_sub_resource(mod_id, module)
            else:
                module = modules[mod_unique_id]
            port = GenericTrafficGeneratorPort(shell_name, "Port {}".format(port_id), port_unique_id)
            module.add_sub_resource(port_id, port)
        return root_resource
