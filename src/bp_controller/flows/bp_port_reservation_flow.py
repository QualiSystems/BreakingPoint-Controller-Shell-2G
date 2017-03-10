from xml.etree import ElementTree
from bp_controller.actions.port_reservation_actions import PortReservationActions
from bp_controller.actions.test_configuration_actions import TestConfigurationActions
from bp_controller.actions.test_execution_actions import TestExecutionActions
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow


class BPPortReservationFlow(BPFlow):
    def reserve_ports(self, group, ports):
        with self._session_manager.get_session() as rest_service:
            port_reservation = PortReservationActions(rest_service, self._logger)
            results = []
            for slot, port in ports:
                result = port_reservation.reserve_port(slot, [port], group)

    def unreserve_ports(self, ports):
        with self._session_manager.get_session() as rest_service:
            port_reservation = PortReservationActions(rest_service, self._logger)
            results = []
            for slot, port in ports:
                result = port_reservation.unreserve_port(slot, [port])
