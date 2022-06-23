from cloudshell_bp.tg.breaking_point.rest_actions.rest_actions import RestActions


class AutoloadActions(RestActions):
    def get_ports_info(self):
        self._logger.debug("Ports info request")
        uri = "/api/v1/bps/ports"
        data = self._rest_service.request_get(uri)
        result = data.get("portReservationState")
        return result
