# coding:utf-8
import json
import inspect

import tornado.web
import tornado.gen
import functools
import abc


class RestFulApiGenerator(type):
    METHOD_MAP = {'get': 'read', 'post': 'create',
                  'put': 'update', 'delete': 'delete'}

    api_route = [

    ]

    """ automatically generate api route

        GET & POST wrap_original to /schema
        PUT & DELETE wrap_original to /schema/*pk_pattern*

        Query Some One for /schema/_search
        List All  /schema/_list?start=0&count=10



    """

    route2handler = {
        "read/write": ("POST", "GET"),
        "update/delete": ("PUT", "DELETE"),
        "list": ()

    }

    api_prefix = ''

    def __new__(mcs, name, bases, attributes):
        # print name, bases, attributes
        for http_method, instance_method in mcs.METHOD_MAP.items():
            if attributes.has_key(instance_method):
                attributes[http_method] = mcs.wrap_original(attributes[instance_method])
        return type.__new__(mcs, name, bases, attributes)

    @classmethod
    def wrap_original(mcs, method):
        """
        return http request handling method
        :param method:
        :return:
        """

        def handler_request(*args, **kwargs):
            instance = args[0]
            try:
                if inspect.isgenerator(method):
                    tornado.gen.coroutine(method)
                else:
                    instance.build_response(method(*args, **kwargs))
            except Exception, error:
                return instance.handler_error(error)

        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            instance = args[0]
            for mt in [mcs.logging_process(instance.prepare_request),
                       lambda: handler_request(*args, **kwargs),
                       mcs.logging_process(instance.finish_request)]:
                print instance, "Execute", mt
                mt()

        return wrapper

    @classmethod
    def building_api(mcs, name, bases, attributes, methods):
        pass

    @classmethod
    def add_handler_to_route(mcs, handler, route):
        mcs.api_route.append((route, handler))

    @classmethod
    def logging_process(mcs, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except Exception, e:
                print "EEE", e
                pass
                # TODO logging

        return wrapper


class BaseRequestLoader(object):
    def load(self, body):
        pass


class BaseResponseBuilder(object):
    def build(self, obj):
        """
        return string
        :param data:
        :return: string
        """
        print obj, "OOOO"
        return json.dumps(obj)


class Resource(tornado.web.RequestHandler):
    __metaclass__ = RestFulApiGenerator
    SUPPORTED_METHODS = set(tornado.web.RequestHandler.SUPPORTED_METHODS)

    response_string = ""
    request_obj = None

    @classmethod
    def allow(cls, methods):
        """
        return subclass of current class , block methods not allowed
        :param methods:
        :return:
        """
        if isinstance(methods, basestring):
            methods = [methods]
        methods = set([_.upper() for _ in methods])
        blocked = cls.SUPPORTED_METHODS - methods
        new_class = type(cls.__name__, (cls,), {})
        for blocked_method in blocked:
            setattr(new_class, blocked_method, getattr(tornado.web.RequestHandler, blocked_method.lower()))
        return new_class

    def prepare_request(self):
        if self.request.method in {"POST", "PUT"}:
            self.load_request()
        else:
            pass

    def load_request(self):
        self.request_obj = json.loads(self.request.body)

    def build_response(self, obj):
        self.response_string = json.dumps(obj)

    def finish_request(self):
        self.write(self.response_string)

    def initialize(self):
        pass

    def read(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def query(self):
        pass

    def list_all(self):
        pass

    def handler_error(self, error):
        print error


class ORMInterface(object):
    def create(self):
        pass

    def update(self):
        pass

    def read(self):
        pass

    def delete(self):
        pass


class ResourceInterface(object):
    def from_json(self, jdata):
        """
        :param jdata: dict instance
        :return:
        """

    def to_json(self):
        """

        :return:
        """
