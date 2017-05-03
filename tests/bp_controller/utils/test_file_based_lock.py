from mock import patch, Mock
from unittest2 import TestCase

from bp_controller.utils.file_based_lock import FileBasedLock


class TestFileBasedLock(TestCase):
    def setUp(self):
        self._file_path = Mock()
        self._file_descriptor = Mock()
        self._instance = self._create_instance()

    # @patch('bp_controller.utils.file_based_lock.open')
    @patch('__builtin__.open')
    def _create_instance(self, open_func):
        open_func.return_value = self._file_descriptor
        instance = FileBasedLock(self._file_path)
        open_func.assert_called_once_with(self._file_path, 'w')
        return instance

    def test_init(self):
        self.assertIs(self._instance._file_descriptor, self._file_descriptor)

    @patch('bp_controller.utils.file_based_lock.portalocker')
    def test_enter_exit(self, portalocker):
        lock_ex = Mock()
        portalocker.LOCK_EX = lock_ex
        with self._instance:
            pass
        portalocker.lock.assert_called_once_with(self._file_descriptor, lock_ex)
        self._file_descriptor.close.assert_called_once_with()
