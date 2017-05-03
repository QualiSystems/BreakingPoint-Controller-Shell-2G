from mock import patch, Mock
from unittest2 import TestCase, skip

from driver import BreakingPointControllerDriver


class TestRunnerContext(object):
    def __init__(self, instance):
        self._instance = instance

    def __enter__(self):
        return self._instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TestDriver(TestCase):
    def setUp(self):
        self._runners_pool = Mock()
        self._instance = self._create_instance()
        self._context = Mock()
        self._runner = Mock()
        self._runners_pool.actual_runner.return_value = TestRunnerContext(self._runner)

    @patch('driver.BPRunnersPool')
    def _create_instance(self, runners_pool_class):
        runners_pool_class.return_value = self._runners_pool
        return BreakingPointControllerDriver()

    def test_init(self):
        self.assertIs(self._instance._runners_pool, self._runners_pool)

    @patch('driver.AutoLoadDetails')
    def test_get_inventory(self, autoload_details_class):
        autoload_details = Mock()
        autoload_details_class.return_value = autoload_details
        self.assertIs(self._instance.get_inventory(self._context), autoload_details)

    def test_load_config(self):
        result = Mock()
        self._runner.load_configuration.return_value = result
        config_file = '"test/test"'
        self.assertIs(self._instance.load_config(self._context, config_file), result)
        self._runners_pool.actual_runner.assert_called_once_with(self._context)
        self._runner.load_configuration.assert_called_once_with(config_file.strip('"'))

    def test_start_traffic(self):
        result = Mock()
        self._runner.start_traffic.return_value = result
        self.assertIs(self._instance.start_traffic(self._context, True), result)
        self._runners_pool.actual_runner.assert_called_once_with(self._context)
        self._runner.start_traffic.assert_called_once_with(True)

    def test_stop_traffic(self):
        result = Mock()
        self._runner.stop_traffic.return_value = result
        self.assertIs(self._instance.stop_traffic(self._context), result)
        self._runners_pool.actual_runner.assert_called_once_with(self._context)
        self._runner.stop_traffic.assert_called_once_with()

    def test_get_statistics(self):
        result = Mock()
        self._runner.get_statistics.return_value = result
        view_name = Mock()
        output_type = Mock()
        self.assertIs(self._instance.get_statistics(self._context, view_name, output_type), result)
        self._runners_pool.actual_runner.assert_called_once_with(self._context)
        self._runner.get_statistics.assert_called_once_with(view_name, output_type)

    def test_get_results(self):
        result = Mock()
        self._runner.get_results.return_value = result
        self.assertIs(self._instance.get_results(self._context), result)
        self._runners_pool.actual_runner.assert_called_once_with(self._context)
        self._runner.get_results.assert_called_once_with()

    def test_cleanup(self):
        self._instance.cleanup()
        self._runners_pool.close_all_runners.assert_called_once_with()

    def test_keep_alive(self):
        cancellation_context = Mock()
        cancellation_context.is_cancelled = True
        result = Mock()
        self._runner.close.return_value = result
        self.assertIs(self._instance.keep_alive(self._context, cancellation_context), result)
        self._runners_pool.actual_runner.assert_called_once_with(self._context)
        self._runner.close.assert_called_once_with()
