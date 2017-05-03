from mock import Mock, patch
from unittest2 import TestCase

from bp_controller.runners.bp_runner_pool import InstanceLocker, BPRunnersPool


class TestInstanceLocker(TestCase):
    def setUp(self):
        self._lock = Mock()
        self._locked_instance = Mock()
        self._instance = self._create_instance()

    @patch('bp_controller.runners.bp_runner_pool.Lock')
    def _create_instance(self, lock_class):
        lock_class.return_value = self._lock
        instance = InstanceLocker(self._locked_instance)
        lock_class.assert_called_once_with()
        return instance

    def test_init(self):
        self.assertIs(self._instance._instance, self._locked_instance)

    def test_instance_prop(self):
        self.assertIs(self._instance.instance, self._locked_instance)

    def test_enter_exit(self):
        with self._instance as instance:
            self.assertIs(instance, self._locked_instance)
        self._lock.acquire.assert_called_once_with()
        self._lock.release.assert_called_once_with()


class TestBPRunnersPool(TestCase):
    def setUp(self):
        self._context = Mock()
        self._instance = BPRunnersPool()

    def test_init(self):
        self.assertEqual(self._instance._runners, {})

    @patch('bp_controller.runners.bp_runner_pool.InstanceLocker')
    @patch('bp_controller.runners.bp_runner_pool.BPTestRunner')
    @patch('bp_controller.runners.bp_runner_pool.get_logger_with_thread_id')
    @patch('bp_controller.runners.bp_runner_pool.get_api')
    def test_actual_runner_call_logger_and_api(self, get_api_func, get_logger_func, test_runner_class,
                                               instance_locker_class):
        actual_runner = self._instance.actual_runner(self._context)
        get_api_func.assert_called_once_with(self._context)
        get_logger_func.assert_called_once_with(self._context)

    @patch('bp_controller.runners.bp_runner_pool.InstanceLocker')
    @patch('bp_controller.runners.bp_runner_pool.BPTestRunner')
    @patch('bp_controller.runners.bp_runner_pool.get_logger_with_thread_id')
    @patch('bp_controller.runners.bp_runner_pool.get_api')
    def test_actual_runner_new_instance(self, get_api_func, get_logger_func, test_runner_class,
                                        instance_locker_class):
        logger_instance = Mock()
        api_instance = Mock()
        get_logger_func.return_value = logger_instance
        get_api_func.return_value = api_instance
        instance_locker_inst = Mock()
        test_runner_inst = Mock()
        instance_locker_class.return_value = instance_locker_inst
        test_runner_class.return_value = test_runner_inst
        reservation_id = Mock()
        self._context.reservation.reservation_id = reservation_id
        self.assertIs(self._instance.actual_runner(self._context), instance_locker_inst)
        instance_locker_class.assert_called_once_with(test_runner_inst)
        test_runner_class.assert_called_once_with(self._context, logger_instance, api_instance)
        self.assertIs(self._instance._runners[reservation_id], instance_locker_inst)

    @patch('bp_controller.runners.bp_runner_pool.InstanceLocker')
    @patch('bp_controller.runners.bp_runner_pool.BPTestRunner')
    @patch('bp_controller.runners.bp_runner_pool.get_logger_with_thread_id')
    @patch('bp_controller.runners.bp_runner_pool.get_api')
    def test_actual_runner_existing_instance(self, get_api_func, get_logger_func, test_runner_class,
                                             instance_locker_class):
        logger_instance = Mock()
        api_instance = Mock()
        get_logger_func.return_value = logger_instance
        get_api_func.return_value = api_instance
        reservation_id = Mock()
        self._context.reservation.reservation_id = reservation_id
        runner_instance = Mock()
        self._instance._runners[reservation_id] = runner_instance
        runner_locker = self._instance.actual_runner(self._context)
        self.assertIs(runner_locker, runner_instance)
        self.assertIs(runner_locker.instance.logger, logger_instance)
        self.assertIs(runner_locker.instance.api, api_instance)
        self.assertIs(runner_locker.instance.context, self._context)

    def test_class_all_runners(self):
        runner = Mock()
        self._instance._runners[Mock()] = runner
        self._instance.close_all_runners()
        runner.close.assert_called_once_with()
