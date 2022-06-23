#!/usr/bin/python
# -*- coding: utf-8 -*-
from functools import wraps

import jsonpickle
from urlparse import urlsplit, urlunsplit


def validate_vlan_number(number):
    try:
        if int(number) > 4000 or int(number) < 1:
            return False
    except ValueError:
        return False
    return True


def validate_vlan_range(vlan_range):
    result = None
    for vlan in vlan_range.split(","):
        if "-" in vlan:
            for vlan_range_border in vlan.split("-"):
                result = validate_vlan_number(vlan_range_border)
        else:
            result = validate_vlan_number(vlan)
        if not result:
            return False
    return True


def serialize_to_json(result, unpicklable=False):
    """Serializes output as JSON and writes it to console output wrapped with special prefix and suffix

    :param result: Result to return
    :param unpicklable: If True adds JSON can be deserialized as real object.
                        When False will be deserialized as dictionary
    """

    json = jsonpickle.encode(result, unpicklable=unpicklable)
    result_for_output = str(json)
    return result_for_output


class UrlParser(object):
    SCHEME = "scheme"
    NETLOC = "netloc"
    PATH = "path"
    FILENAME = "filename"
    QUERY = "query"
    FRAGMENT = "fragment"
    USERNAME = "username"
    PASSWORD = "password"
    HOSTNAME = "hostname"
    PORT = "port"

    @staticmethod
    def parse_url(url):
        parsed = urlsplit(url)
        result = {}
        for attr in dir(UrlParser):
            if attr.isupper() and not attr.startswith("_"):
                attr_value = getattr(UrlParser, attr)
                if hasattr(parsed, attr_value):
                    value = getattr(parsed, attr_value)
                    if attr_value == UrlParser.PATH:
                        path = value
                        result[UrlParser.FILENAME] = ""
                        if not path.endswith("/"):
                            filename = path[path.rfind("/") + 1 :]
                            result[UrlParser.FILENAME] = filename
                            path = path.replace(filename, "")
                        result[UrlParser.PATH] = path[:-1]
                    else:
                        result[attr_value] = value
        return result

    @staticmethod
    def build_url(url):
        if not url:
            raise Exception("Url dictionary is empty.")
        scheme = url.get(UrlParser.SCHEME, "")
        query = url.get(UrlParser.QUERY, "")
        fragment = url.get(UrlParser.FRAGMENT, "")
        netloc = url.get(UrlParser.NETLOC)
        host = url.get(UrlParser.HOSTNAME, "")
        port = url.get(UrlParser.PORT)
        username = url.get(UrlParser.USERNAME)
        password = url.get(UrlParser.PASSWORD)
        path = url.get(UrlParser.PATH, "")
        filename = url.get(UrlParser.FILENAME, "")

        if not scheme:
            raise Exception("Url missing key value: scheme.")

        if not netloc:
            netloc = host
        if port and str(port) not in netloc:
            netloc += ":{}".format(port)
        if username and username not in netloc or password and password not in netloc:
            credentials = "{}@".format(username)
            if password:
                credentials = "{}:{}@".format(username, password)
            netloc = credentials + netloc

        target_path = filename
        if path:
            if not path.endswith("/"):
                path = "{}/".format(path)
            target_path = path + target_path

        return urlunsplit((scheme, netloc, target_path, query, fragment))


def command_logging(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        func_name = func.__name__

        self._logger.info('Start command "{}"'.format(func_name))
        finishing_msg = 'Command "{}" finished {}'
        try:
            result = func(self, *args, **kwargs)
        except Exception:
            self._logger.info(finishing_msg.format(func_name, "unsuccessfully"))
            raise
        else:
            self._logger.info(finishing_msg.format(func_name, "successfully"))

        return result

    return wrapped
