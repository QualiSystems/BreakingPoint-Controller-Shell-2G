import os
import portalocker


class FileBasedLock(object):
    def __init__(self, lock_file_path):
        if os.path.exists(lock_file_path):
            self.__file_descriptor = open(lock_file_path, 'r')
        else:
            self.__file_descriptor = open(lock_file_path, 'w')

    def __enter__(self):
        portalocker.lock(self.__file_descriptor, portalocker.LOCK_EX)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__file_descriptor.close()
