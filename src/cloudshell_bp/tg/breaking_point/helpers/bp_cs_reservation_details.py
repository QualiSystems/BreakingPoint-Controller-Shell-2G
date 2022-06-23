#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from cloudshell_bp.tg.breaking_point.bp_exception import BPException


class BPCSReservationDetails(object):
    PORT_FAMILY = [
        "Port",
        "Virtual Port",
        "Breaking Point Virtual Port",
        "CS_TrafficGeneratorPort",
        "CS_VirtualTrafficGeneratorPort",
    ]
    STATIC_VM_PORT = {"family_name": "CS_Port", "model_name": "BP vBlade.GenericVPort"}
    CHASSIS_FAMILY = [
        "Traffic Generator Chassis",
        "Virtual Traffic Generator Chassis",
        "CS_TrafficGeneratorChassis",
        "CS_VirtualTrafficGeneratorChassis",
    ]
    STATIC_VM_CHASSIS = {"family_name": "CS_GenericAppFamily", "model_name": "BP vChassis"}
    PORT_ATTRIBUTE = "Logical Name"
    USERNAME_ATTRIBUTE = "User"
    PASSWORD_ATTRIBUTE = "Password"

    def __init__(self, reservation_id, logger, api):
        self._reservation_id = reservation_id
        self._logger = logger
        self._api = api

        self._reservation_details = None
        self._resource_details_dict = {}
        self.__chassis_resource = None

    @property
    def api(self):
        return self._api

    @property
    def logger(self):
        return self._logger

    @property
    def _chassis_resource(self):
        if not self.__chassis_resource:
            self.__chassis_resource = self._find_chassis_resource()
        return self.__chassis_resource

    @property
    def _chassis_name(self):
        return self._chassis_resource.Name

    @property
    def _chassis_model_name(self):
        return self._chassis_resource.ResourceModelName

    def _find_chassis_resource(self):
        chassis_resource = None
        for resource in self._get_reservation_details().ReservationDescription.Resources:
            if (
                resource.ResourceFamilyName in self.CHASSIS_FAMILY
                or resource.ResourceFamilyName == self.STATIC_VM_CHASSIS["family_name"]
                and resource.ResourceModelName == self.STATIC_VM_CHASSIS["model_name"]
            ):
                chassis_resource = resource
        if not chassis_resource:
            raise BPException(
                self.__class__.__name__, "Cannot find {0} in the reservation".format(", ".join(self.CHASSIS_FAMILY))
            )
        return chassis_resource

    def _get_reservation_details(self):
        if not self._reservation_details:
            self._reservation_details = self.api.GetReservationDetails(reservationId=self._reservation_id)
        return self._reservation_details

    def _get_resource_details(self, resource_name):
        details = self._resource_details_dict.get(resource_name, None)
        if not details:
            details = self.api.GetResourceDetails(resource_name)
            self._resource_details_dict[resource_name] = details
        return details

    def _get_attribute_value(self, resource_name, attribute_name):
        resource_details = self._get_resource_details(resource_name)
        model_attribute_2g = "{}.{}".format(resource_details.ResourceModelName, attribute_name)
        family_attribute_2g = "{}.{}".format(resource_details.ResourceFamilyName, attribute_name)
        for attribute in resource_details.ResourceAttributes:
            if (
                attribute.Name == attribute_name
                or attribute.Name == model_attribute_2g
                or attribute.Name == family_attribute_2g
            ):
                return attribute.Value

    def get_chassis_address(self):
        return self._chassis_resource.FullAddress

    def get_chassis_ports(self):
        self.logger.debug("Api: {}".format(self.api))
        reserved_ports = {}
        port_pattern = r"{}[\\/]M(?P<module>\d+)/P(?P<port>\d+)".format(self.get_chassis_address())
        for resource in self._get_reservation_details().ReservationDescription.Resources:
            if (
                resource.ResourceFamilyName in self.PORT_FAMILY
                or resource.ResourceFamilyName == self.STATIC_VM_PORT["family_name"]
                and resource.ResourceModelName == self.STATIC_VM_PORT["model_name"]
            ):
                result = re.search(port_pattern, resource.FullAddress)
                if result:
                    logical_name = self._get_attribute_value(resource.Name, self.PORT_ATTRIBUTE)
                    if logical_name:
                        reserved_ports[logical_name.lower()] = (result.group("module"), result.group("port"))

            if (
                resource.ResourceFamilyName == self.STATIC_VM_PORT["family_name"]
                and resource.ResourceModelName == self.STATIC_VM_PORT["model_name"]
            ):
                result = re.search(port_pattern, resource.FullAddress)
                if result:
                    logical_name = self._get_attribute_value(resource.Name, self.PORT_ATTRIBUTE)
                    # 'BP vBlade.GenericVPort.Logical Name'
                    if logical_name:
                        reserved_ports[logical_name.lower()] = (result.group("module"), result.group("port"))

        self.logger.debug("Chassis ports {}".format(reserved_ports))
        return reserved_ports

    def get_chassis_user(self):
        username = self._get_attribute_value(self._chassis_name, self.USERNAME_ATTRIBUTE)
        self.logger.debug("Chassis username {}".format(username))
        return username

    def get_chassis_password(self):
        encrypted_password = self._get_attribute_value(self._chassis_name, self.PASSWORD_ATTRIBUTE)
        chassis_password = self.api.DecryptPassword(encrypted_password).Value
        self.logger.debug("Chassis Password {}".format(chassis_password))
        return chassis_password
