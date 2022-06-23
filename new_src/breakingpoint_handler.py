"""
STC controller shell business logic.
"""
# pylint: disable=arguments-differ
import csv
import io
import logging
from collections import OrderedDict
from pathlib import Path
from typing import Union, Optional
from xml.etree import ElementTree

import requests
from cloudshell.shell.core.driver_context import ResourceCommandContext
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.traffic.helpers import get_family_attribute, get_location, get_resources_from_reservation
from cloudshell.traffic.rest_api_helpers import RestClientUnauthorizedException, RestClientException
from cloudshell.traffic.tg import STC_CHASSIS_MODEL, TgControllerHandler, attach_stats_csv, is_blocking
from requests import Response

from breakingpoint_data_model import BreakingpointControllerShell2G

OFFLINE_PORT_MARKER = "offline-debug"


class BreakingPointRestClient:

    def __init__(self, address: str, username: str, password: str, version: int, logger: logging.Logger) -> None:
        super().__init__()
        self.logger = logger
        self.logger.debug('Login request with  Username: {0}, Password: {1}'.format(username, password))
        self.session = requests.Session()
        session_url = f"https://{address}/api/v1/auth/session"
        self.bps_session = self.post(session_url, json={"username": username, "password": password})
        if version == 1:
            self.base_url = f"https://{address}/api/v1"
        else:
            session_id = self.get(self.bps_session["userAccountUrl"])["id"]
            self.base_url = f"https://{address}/bps/api/v2/sessions/{session_id}"

    def get(self, url: str) -> dict:
        return self._valid(self.session.get(self._build_url(url), verify=False))

    def post(self, url: str, data: Optional[dict] = None, json: Optional[dict] = None, **kwargs: object) -> dict:
        return self._valid(self.session.post(self._build_url(url), data=data, json=json, verify=False, **kwargs))

    def _build_url(self, url: str) -> str:
        """Build full URL for the requested REST API command."""
        return url if "https" in url else f"{self.base_url}/{url.lstrip('/')}"

    @staticmethod
    def _valid(response: Response) -> dict:
        """Validate REST response and return the response json if valid response."""
        if response.status_code in [200, 201, 204]:
            return response.json()
        if response.status_code in [401]:
            raise RestClientUnauthorizedException("Incorrect login or password")
        raise RestClientException(f"Request failed: {response.status_code}, {response.text}")


class BreakingPointHandler(TgControllerHandler):
    """BreakingPoint controller shell business logic."""

    def __init__(self) -> None:
        """Initialize object variables, actual initialization is performed in initialize method."""
        super().__init__()
        self.rest_client: BreakingPointRestClient = None

    def initialize(self, context: ResourceCommandContext, logger: logging.Logger) -> None:
        """Init StcApp and connect to STC REST server."""
        service = BreakingpointControllerShell2G.create_from_context(context)
        super().initialize(context, logger, service)

        controller = self.service.address
        user = self.service.user
        self.logger.debug(f"Controller - {self.service.address}")
        self.logger.debug(f"User - {user}")
        self.logger.debug(f"Encrypted password - {self.resource.password}")
        password = CloudShellSessionContext(context).get_api().DecryptPassword(self.resource.password).Value
        self.logger.debug(f"Password - {password}")
        self.rest_client = BreakingPointRestClient(controller, user, password, version=1, logger=self.logger)

    def cleanup(self) -> None:
        """Disconnect from BreakingPoint REST server."""

    def load_config(self, _: ResourceCommandContext, breakingpoint_test_file_name: str) -> None:
        """Load STC configuration file, and map and reserve ports."""
        self.logger.debug(f'Uploading test {breakingpoint_test_file_name}')

        data = {'force': True}
        name = Path(breakingpoint_test_file_name).name
        files = {'file': (name, open(breakingpoint_test_file_name, 'rb'))}
        self.rest_client.post('bps/upload', data=data, files=files)

        test_model = ElementTree.parse(Path(breakingpoint_test_file_name).as_posix()).getroot().find('testmodel')
        network_name = test_model.get('network')
        interfaces = []
        for interface in test_model.findall('interface'):
            interfaces.append(int(interface.get('number')))
        self._port_reservation_helper.reserve_ports(network_name, interfaces, self._bp_session)

    def load_config_stc(self, context: ResourceCommandContext, stc_config_file_name: str) -> None:
        """Load STC configuration file, and map and reserve ports."""
        self.stc.load_config(stc_config_file_name)
        config_ports = self.stc.project.get_ports()

        reservation_ports = {}
        for port in get_resources_from_reservation(context, f"{STC_CHASSIS_MODEL}.GenericTrafficGeneratorPort"):
            reservation_ports[get_family_attribute(context, port.Name, "Logical Name")] = port

        for name, port in config_ports.items():
            if name in reservation_ports:
                address = get_location(reservation_ports[name])
                self.logger.debug(f"Logical Port {name} will be reserved on Physical location {address}")
                if OFFLINE_PORT_MARKER not in reservation_ports[name].Name:
                    port.reserve(address, force=True, wait_for_up=False)
                else:
                    self.logger.debug(f"Offline debug port {address} - no actual reservation")
            else:
                raise TgnError(f'Configuration port "{port}" not found in reservation ports {reservation_ports.keys()}')

        self.logger.info("Port Reservation Completed")

    def send_arp(self) -> None:
        """Send ARP/ND for all devices and streams."""
        self.stc.send_arp_ns()

    def start_devices(self) -> None:
        """Start all emulations on all devices."""
        self.stc.start_devices()

    def stop_devices(self) -> None:
        """Stop all emulations on all devices."""
        self.stc.stop_devices()

    def start_traffic(self, blocking: str) -> None:
        """Start traffic on all ports."""
        self.stc.clear_results()
        self.stc.start_traffic(is_blocking(blocking))

    def stop_traffic(self) -> None:
        """Stop traffic on all ports."""
        self.stc.stop_traffic()

    def get_statistics(self, context: ResourceCommandContext, view_name: str, output_type: str) -> Union[dict, str]:
        """Start traffic on all ports."""
        stats_obj = StcStats(view_name)
        stats_obj.read_stats()
        statistics = OrderedDict()
        for obj, obj_values in stats_obj.statistics.items():
            statistics[obj.name] = obj_values

        if output_type.strip().lower() == "json":
            statistics_str = json.dumps(statistics, indent=4, sort_keys=True, ensure_ascii=False)
            return json.loads(statistics_str)
        if output_type.strip().lower() == "csv":
            captions = list(list(statistics.values())[0].keys())
            output = io.StringIO()
            writer = csv.DictWriter(output, captions)
            writer.writeheader()
            for obj_values in statistics.values():
                writer.writerow(obj_values)
            attach_stats_csv(context, self.logger, view_name, output.getvalue().strip())
            return output.getvalue().strip()
        raise TgnError(f'Output type should be CSV/JSON - got "{output_type}"')

    def sequencer_command(self, command: str) -> None:
        """Run sequencer command."""
        if StcSequencerOperation[command.lower()] == StcSequencerOperation.start:
            self.stc.clear_results()
        self.stc.sequencer_command(StcSequencerOperation[command.lower()])

    def get_session_id(self) -> str:
        """Return the REST session ID."""
        self.logger.info(f"session_id = {self.stc.api.session_id}")
        return self.stc.api.session_id

    def get_children(self, obj_ref: str, child_type: str) -> list:
        """Return all children, of the requested type, of the requested object."""
        children_attribute = "children-" + child_type if child_type else "children"
        return self.stc.api.client.get(obj_ref, children_attribute).split()

    def get_attributes(self, obj_ref: str) -> dict:
        """Return all attributes of the requested object."""
        return self.stc.api.client.get(obj_ref)

    def set_attribute(self, obj_ref: str, attr_name: str, attr_value: str) -> None:
        """Set object attribute."""
        self.stc.api.client.config(obj_ref, **{attr_name: attr_value})

    def perform_command(self, command: str, parameters_json: str) -> str:
        """Perform STC command."""
        return self.stc.api.client.perform(command, json.loads(parameters_json))
