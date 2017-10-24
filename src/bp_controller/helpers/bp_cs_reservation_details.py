#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from cloudshell.tg.breaking_point.bp_exception import BPException


class BPCSReservationDetails(object):
    PORT_FAMILY = ['Port', 'Virtual Port']
    CHASSIS_FAMILY = ['Traffic Generator Chassis', 'Virtual Traffic Generator Chassis']
    PORT_ATTRIBUTE = 'Logical Name'
    USERNAME_ATTRIBUTE = 'User'
    PASSWORD_ATTRIBUTE = 'Password'

    def __init__(self, context, logger, api):
        self._context = context
        self._logger = logger
        self._api = api

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        self._api = value

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    def get_chassis_address(self):
        for resource in self._get_reservation_details().ReservationDescription.Resources:
            if resource.ResourceFamilyName in self.CHASSIS_FAMILY:
                chassis_address = resource.FullAddress
                self.logger.debug('Chassis address {}'.format(chassis_address))
                return chassis_address
        raise BPException(self.__class__.__name__, 'Cannot find {0} in this reservation'.format(self.CHASSIS_FAMILY))

    def _get_chassis_name(self):
        for resource in self._get_reservation_details().ReservationDescription.Resources:
            if resource.ResourceFamilyName in self.CHASSIS_FAMILY:
                return resource.Name
        raise BPException(self.__class__.__name__, 'Cannot find {0} in this reservation'.format(self.CHASSIS_FAMILY))

    def _get_reservation_details(self):
        self.logger.debug('API instance: {}'.format(self.api))
        reservation_id = self.context.reservation.reservation_id
        return self.api.GetReservationDetails(reservationId=reservation_id)

    def get_chassis_ports(self):
        self.logger.debug('Api: {}'.format(self.api))
        reserved_ports = {}
        port_pattern = r'{}/M(?P<module>\d+)/P(?P<port>\d+)'.format(self.get_chassis_address())
        for resource in self._get_reservation_details().ReservationDescription.Resources:
            if resource.ResourceFamilyName in self.PORT_FAMILY:
                result = re.search(port_pattern, resource.FullAddress)
                if result:
                    logical_name = self.api.GetAttributeValue(resourceFullPath=resource.Name,
                                                              attributeName=self.PORT_ATTRIBUTE).Value
                    if logical_name:
                        reserved_ports[logical_name.lower()] = (result.group('module'), result.group('port'))
        self.logger.debug('Chassis ports {}'.format(reserved_ports))
        return reserved_ports

    @staticmethod
    def _find_attribute(attribute_name, attribute_list):
        for attribute in attribute_list:
            if attribute.Name == attribute_name:
                return attribute.Value

    def get_chassis_user(self):
        details = self.api.GetResourceDetails(self._get_chassis_name())
        username = self._find_attribute(self.USERNAME_ATTRIBUTE, details.ResourceAttributes)
        self.logger.debug('Chassis username {}'.format(username))
        return username

    def get_chassis_password(self):
        details = self.api.GetResourceDetails(self._get_chassis_name())
        encrypted_password = self._find_attribute(self.PASSWORD_ATTRIBUTE, details.ResourceAttributes)
        chassis_password = self.api.DecryptPassword(encrypted_password).Value
        self.logger.debug('Chassis Password {}'.format(chassis_password))
        return chassis_password
