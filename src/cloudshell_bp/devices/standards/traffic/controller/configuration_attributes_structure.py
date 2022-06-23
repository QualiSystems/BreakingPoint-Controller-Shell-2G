#!/usr/bin/python
# -*- coding: utf-8 -*-


class GenericTrafficControllerResource(object):
    def __init__(self, shell_name=None, name=None, supported_os=None):
        """Init method

        :param shell_name: Shell Name
        :type shell_name: str
        :param name: Resource Name
        :type name: str
        :param supported_os: list of supported OS
        :type supported_os: list
        """

        self.attributes = {}
        self.shell_name = shell_name
        self.name = name
        self.supported_os = supported_os
        self.fullname = None
        self.address = None  # The IP address of the resource
        self.family = None  # The resource family

        if shell_name:
            self.namespace_prefix = "{}.".format(self.shell_name)
        else:
            self.namespace_prefix = ""

    @property
    def user(self):
        """
        User with administrative privileges
        :rtype: str
        """
        return self.attributes.get("{}User".format(self.namespace_prefix), None)

    @property
    def password(self):
        """
        Password
        :rtype: str
        """
        return self.attributes.get("{}Password".format(self.namespace_prefix), None)

    @property
    def remote_address(self):
        """
        Address for remote access
        :rtype: str
        """
        return self.attributes.get("{}Address".format(self.namespace_prefix), None)

    @property
    def client_install_path(self):
        """
        The path in which the traffic client is installed on the Execution Server.
        For example C:/Program Files (x86)/Ixia/IxLoad/5.10-GA
        :rtype: str
        """
        return self.attributes.get("{}Client Install Path".format(self.namespace_prefix), None)

    @property
    def controller_tcp_port(self):
        """
        The TCP port of the traffic controller. Relevant only in case an external controller is configured.
        Default TCP port should be used if kept empty.
        :rtype: int
        """
        return self.attributes.get("{}Controller TCP Port".format(self.namespace_prefix), None)

    @property
    def test_files_location(self):
        """
        Location for test related files
        :rtype: str
        """
        return self.attributes.get("{}Test Files Location".format(self.namespace_prefix), None)

    @property
    def service_categories(self):
        """
        A list of categories
        :rtype: str
        """
        return self.attributes.get("{}Service Categories".format(self.namespace_prefix), None)

    @classmethod
    def from_context(cls, shell_name, supported_os, context):
        """
        Creates an instance of Networking Resource by given context
        :param shell_name: Shell Name
        :type shell_name: str
        :param supported_os: list of supported OS
        :type supported_os: list
        :param context: cloudshell_bp.shell.core.driver_context.ResourceCommandContext
        :type context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :return:
        :rtype GenericNetworkingResource
        """

        result = cls(shell_name=shell_name, name=context.resource.name, supported_os=supported_os)
        result.address = context.resource.address
        result.family = context.resource.family
        result.fullname = context.resource.fullname

        result.attributes = dict(context.resource.attributes)

        return result
