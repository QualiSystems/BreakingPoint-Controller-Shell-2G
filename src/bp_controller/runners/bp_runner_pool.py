from threading import Lock

from bp_controller.runners.bp_test_runner import BPTestRunner
from cloudshell.tg.breaking_point.helpers.context_utils import get_logger_with_thread_id, get_api


class InstanceLocker(object):
    """
    Lock for each runner instance
    """

    def __init__(self, instance):
        self.__lock = Lock()
        self._instance = instance

    @property
    def instance(self):
        return self._instance

    def __enter__(self):
        """

        :return:
        :rtype: BPTestRunner
        """
        self.__lock.acquire()
        return self._instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__lock.release()


class BPRunnersPool(object):
    """
    Pool for runner instances
    """

    def __init__(self):
        self._runners = {}

    def actual_runner(self, context):
        """
        Return runner instance for specific reservation id
        :param context:
        :return:
        :rtype: InstanceLocker
        """
        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        logger.debug('Token: {}'.format(context.connectivity.admin_auth_token))

        reservation_id = context.reservation.reservation_id
        if reservation_id not in self._runners:
            logger.info("Created new runner for {0}".format(reservation_id))
            runner_locker = InstanceLocker(BPTestRunner(context, logger, api))
            self._runners[reservation_id] = runner_locker
        else:
            logger.info("Getting existing runner for {0}".format(reservation_id))
            runner_locker = self._runners[reservation_id]
            runner_locker.instance.logger = logger
            runner_locker.instance.api = api
            runner_locker.instance.context = context
        return runner_locker

    def close_all_runners(self):
        for runner in self._runners.values():
            runner.close()
