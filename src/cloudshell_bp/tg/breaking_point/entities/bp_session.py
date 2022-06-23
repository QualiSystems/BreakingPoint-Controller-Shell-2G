class BPSession(object):
    test_name = None
    test_id = None
    reserved_ports = []
    reservation_group = None

    def __init__(self, cs_reservation_id):
        self.__cs_reservation_id = cs_reservation_id

    @property
    def cs_reservation_id(self):
        return self.__cs_reservation_id

    def __eq__(self, other):
        """
        :param BPSession other:
        :rtype: bool
        """

        return self.cs_reservation_id == other.cs_reservation_id
