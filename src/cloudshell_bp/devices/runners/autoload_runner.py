#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractproperty

from cloudshell_bp.devices.networking_utils import command_logging
from cloudshell_bp.devices.runners.interfaces.autoload_runner_interface import AutoloadOperationsInterface


class AutoloadRunner(AutoloadOperationsInterface):
    __metaclass__ = ABCMeta

    def __init__(self, resource_config, logger):
        """
        Facilitate SNMP autoload
        :param resource_config:
        :param logging.Logger logger:
        """

        self.resource_config = resource_config
        self._logger = logger

    @abstractproperty
    def autoload_flow(self):
        """Autoload flow property
        :return: AutoloadFlow object
        """

        pass

    def _log_device_details(self, details):
        needed_attrs = {"Vendor", "Model", "OS Version"}
        attrs = {}

        for attr in details.attributes:
            attr_name = attr.attribute_name.rsplit(".", 1)[-1]

            if attr.relative_address == "" and attr_name in needed_attrs:
                attrs[attr_name] = attr.attribute_value

                needed_attrs.remove(attr_name)
                if not needed_attrs:
                    break

        self._logger.info(
            'Device Vendor: "{}", Model: "{}", OS Version: "{}"'.format(
                attrs.get("Vendor", ""),
                attrs.get("Model", ""),
                attrs.get("OS Version", ""),
            )
        )

    @command_logging
    def discover(self):
        """Enable and Disable SNMP communityon the device, Read it's structure and attributes: chassis, modules,
        submodules, ports, port-channels and power supplies

        :return: AutoLoadDetails object
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """

        details = self.autoload_flow.execute_flow(
            self.resource_config.supported_os,
            self.resource_config.shell_name,
            self.resource_config.family,
            self.resource_config.name,
        )

        self._log_device_details(details)
        return details
