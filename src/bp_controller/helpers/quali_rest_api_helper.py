from cloudshell.tg.breaking_point.rest_api.rest_json_client import RestJsonClient


class QualiAPIHelper(object):
    def __init__(self, logger, server_name, domain="Global"):
        self.server_name = server_name
        if ":" not in self.server_name:
            self.server_name += ":9000"
        self.domain = domain
        self.logger = logger
        self.rest_client = RestJsonClient(self.server_name, False)

    def upload_file(self, reservation_id, file_stream, file_name):
        self.remove_attached_files(reservation_id)
        self.attach_new_file(reservation_id, file_stream, file_name)

    def login(self, token):
        """
        Login request
        :param username:
        :param password:
        :return:
        """

        uri = 'API/Auth/Login'
        json_data = {'token': token, 'domain': self.domain}
        result = self.rest_client.request_put(uri, json_data)
        self.rest_client.set_session_headers(authorization="Basic {0}".format(result.replace('"','')))

    def attach_new_file(self, reservation_id, file_stream, file_name):
        file_to_upload = {'QualiPackage': file_stream}
        data = {
            "reservationId": reservation_id,
            "saveFileAs": file_name,
            "overwriteIfExists": "true",
        }

        self.rest_client.request_post_files('API/Package/AttachFileToReservation',
                                            data=data,
                                            files=file_to_upload)

    def get_attached_files(self, reservation_id):
        uri = 'API/Package/GetReservationAttachmentsDetails/{0}'.format(reservation_id)
        return self.rest_client.request_get(uri) or []

    def remove_attached_files(self, reservation_id):
        for file_name in self.get_attached_files(reservation_id):
            file_to_delete = {"reservationId": reservation_id,
                              "FileName": file_name
                              }
            self.rest_client.request_post('API/Package/DeleteFileFromReservation', data=file_to_delete) or []
