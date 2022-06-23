import threading

from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.shell.core.session.logging_session import LoggingSessionContext


def get_logger_with_thread_id(context):
    """
    Create QS Logger for command context AutoLoadCommandContext, ResourceCommandContext
    or ResourceRemoteCommandContext with thread name
    :param context:
    :return:
    """
    logger = LoggingSessionContext.get_logger_for_context(context)
    child = logger.getChild(threading.currentThread().name)
    for handler in logger.handlers:
        child.addHandler(handler)
    child.level = logger.level
    for log_filter in logger.filters:
        child.addFilter(log_filter)
    return child


def get_api(context):
    """

    :param context:
    :return:
    """

    return CloudShellSessionContext(context).get_api()


def parse_custom_commands(command, separator=";"):
    """Parse run custom command string into the commands list

    :param str command: run custom [config] command(s)
    :param str separator: commands separator in the string
    :rtype: list[str]
    """
    if not command:
        return []

    return command.strip(separator).split(separator)
