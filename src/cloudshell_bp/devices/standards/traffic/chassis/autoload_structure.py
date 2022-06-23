#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell_bp.devices.standards.base import AbstractResource
from cloudshell_bp.devices.standards.validators import attr_length_validator

AVAILABLE_SHELL_TYPES = ["CS_TrafficGeneratorChassis"]

__all__ = [
    "TrafficGeneratorChassis",
    "GenericTrafficGeneratorModule",
    "GenericTrafficGeneratorPort",
    "GenericPowerPort",
    "AVAILABLE_SHELL_TYPES",
]


class TrafficGeneratorChassis(AbstractResource):
    RESOURCE_MODEL = "Traffic Generator Chassis"
    RELATIVE_PATH_TEMPLATE = "CH"

    # NAME_TEMPLATE = 'Chassis {}'

    def __init__(self, shell_name, name, unique_id, shell_type="CS_TrafficGeneratorChassis"):
        super(TrafficGeneratorChassis, self).__init__(shell_name, name, unique_id)

        if shell_name:
            self.shell_name = "{}.".format(shell_name)
            if shell_type in AVAILABLE_SHELL_TYPES:
                self.shell_type = "{}.".format(shell_type)
            else:
                raise Exception(
                    self.__class__.__name__,
                    "Unavailable shell type {shell_type}."
                    "Shell type should be one of: {avail}".format(
                        shell_type=shell_type, avail=", ".join(AVAILABLE_SHELL_TYPES)
                    ),
                )
        else:
            self.shell_name = ""
            self.shell_type = ""

    @property
    def model_name(self):
        """Return the catalog name of the device model.
        This attribute will be displayed in CloudShell instead of the CloudShell model."""

        return self.attributes.get("{}Model Name".format(self.shell_type), None)

    @model_name.setter
    @attr_length_validator
    def model_name(self, value=""):
        """Set the catalog name of the device model.
        This attribute will be displayed in CloudShell instead of the CloudShell model."""

        self.attributes["{}Model Name".format(self.shell_type)] = value

    @property
    def serial_number(self):
        """Return the device serial number."""

        return self.attributes.get("{}Serial Number".format(self.shell_type), None)

    @serial_number.setter
    @attr_length_validator
    def serial_number(self, value=""):
        """Set the device serial number."""

        self.attributes["{}Serial Number".format(self.shell_type)] = value

    @property
    def server_description(self):
        """Return the full description of the server.
        Usually includes the OS, exact firmware version and additional characteritics of the device."""

        return self.attributes.get("{}Server Description".format(self.shell_type), None)

    @server_description.setter
    @attr_length_validator
    def server_description(self, value=""):
        """Set the full description of the server.
        Usually includes the OS, exact firmware version and additional characteritics of the device."""

        self.attributes["{}Server Description".format(self.shell_type)] = value

    @property
    def vendor(self):
        """Return the name of the device manufacture."""

        return self.attributes.get("{}Vendor".format(self.shell_type), None)

    @vendor.setter
    @attr_length_validator
    def vendor(self, value):
        """Set the name of the device manufacture."""

        self.attributes["{}Vendor".format(self.shell_type)] = value

    @property
    def version(self):
        """Return the firmware version of the resource."""

        return self.attributes.get("{}Version".format(self.shell_type), None)

    @version.setter
    @attr_length_validator
    def version(self, value):
        """Set the firmware version of the resource."""

        self.attributes["{}Version".format(self.shell_type)] = value


class GenericTrafficGeneratorModule(AbstractResource):
    RESOURCE_MODEL = "Generic Traffic Generator Module"
    RELATIVE_PATH_TEMPLATE = "M"

    @property
    def model_name(self):
        """Return the catalog name of the device model.
        This attribute will be displayed in CloudShell instead of the CloudShell model."""

        return self.attributes.get("{}Model Name".format(self.namespace), None)

    @model_name.setter
    @attr_length_validator
    def model_name(self, value=""):
        """Set the catalog name of the device model.
        This attribute will be displayed in CloudShell instead of the CloudShell model."""

        self.attributes["{}Model Name".format(self.namespace)] = value

    @property
    def version(self):
        """Return the firmware version of the resource."""

        return self.attributes.get("{}Version".format(self.namespace), None)

    @version.setter
    @attr_length_validator
    def version(self, value):
        """Set the firmware version of the resource."""

        self.attributes["{}Version".format(self.namespace)] = value

    @property
    def serial_number(self):
        """Return the serial number of the resource."""

        return self.attributes.get("{}Serial Number".format(self.namespace), None)

    @serial_number.setter
    @attr_length_validator
    def serial_number(self, value=""):
        """Set the serial number of the resource."""

        self.attributes["{}Serial Number".format(self.namespace)] = value


class GenericTrafficGeneratorPort(AbstractResource):
    RESOURCE_MODEL = "Generic Traffic Generator Port"
    RELATIVE_PATH_TEMPLATE = "P"

    @property
    def media_type(self):
        """
        Return interface media type. Possible values are Fiber and/or Copper (comma-separated).
        :rtype: str
        """
        return self.attributes.get("{}Media Type".format(self.namespace), False)

    @media_type.setter
    @attr_length_validator
    def media_type(self, value):
        """
        Set interface media type. Possible values are Fiber and/or Copper (comma-separated).
        :type value: str
        """
        self.attributes["{}Media Type".format(self.namespace)] = value

    @property
    def configured_controllers(self):
        """
        Return the value which specifies what controller can be used with the ports (IxLoad controller, BP controller etc...)
        :rtype: float
        """
        return self.attributes.get("{}Configured Controllers".format(self.namespace), False)

    @configured_controllers.setter
    @attr_length_validator
    def configured_controllers(self, value):
        """
        Set the value which specifies what controller can be used with the ports (IxLoad controller, BP controller etc...)
        :type value: float
        """
        self.attributes["{}Configured Controllers".format(self.namespace)] = value


class GenericPowerPort(AbstractResource):
    RESOURCE_MODEL = "Generic Power Port"
    RELATIVE_PATH_TEMPLATE = "PP"

    @property
    def model(self):
        """
        Return the device model. This information is typically used for abstract resource filtering.
        :rtype: str
        """
        return self.attributes.get("{}Model".format(self.namespace), False)

    @model.setter
    @attr_length_validator
    def model(self, value):
        """
        Set the device model. This information is typically used for abstract resource filtering.
        :type value: str
        """
        self.attributes["{}Model".format(self.namespace)] = value

    @property
    def model_name(self):
        """Return the catalog name of the device model.
        This attribute will be displayed in CloudShell instead of the CloudShell model.
        :rtype: str"""

        return self.attributes.get("{}Model Name".format(self.namespace), None)

    @model_name.setter
    @attr_length_validator
    def model_name(self, value=""):
        """Set the catalog name of the device model.
        This attribute will be displayed in CloudShell instead of the CloudShell model."""

        self.attributes["{}Model Name".format(self.namespace)] = value

    @property
    def serial_number(self):
        """
        Return the serial number of the resource.
        :rtype: str
        """
        return self.attributes.get("{}Serial Number".format(self.namespace), False)

    @serial_number.setter
    @attr_length_validator
    def serial_number(self, value):
        """
        Set the serial number of the resource.
        :type value: str
        """
        self.attributes["{}Serial Number".format(self.namespace)] = value

    @property
    def version(self):
        """
        Return the firmware version of the resource.
        :rtype: str
        """
        return self.attributes.get("{}Version".format(self.namespace), False)

    @version.setter
    @attr_length_validator
    def version(self, value):
        """
        Set the firmware version of the resource.
        :type value: str
        """
        self.attributes["{}Version".format(self.namespace)] = value

    @property
    def port_description(self):
        """
        Return the description of the port as configured in the device.
        :rtype: str
        """
        return self.attributes.get("{}Port Description".format(self.namespace), False)

    @port_description.setter
    @attr_length_validator
    def port_description(self, value):
        """
        Set the description of the port as configured in the device.
        :type value: str
        """
        self.attributes["{}Port Description".format(self.namespace)] = value
