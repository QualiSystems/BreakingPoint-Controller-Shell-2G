import portalocker


class FileBasedLock(object):
    def __init__(self, lock_file_path):
        self._file_descriptor = open(lock_file_path, 'w')

    def __enter__(self):
        portalocker.lock(self._file_descriptor, portalocker.LOCK_EX)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file_descriptor.close()
