# coding:utf-8
import json
import inspect

import tornado.web
import tornado.gen
from tornado.log import gen_log

import functools
import abc
import utils


class HandlerWrapper(type):
    """ automatically generate api route

        GET & POST wrap_original to /schema
        PUT & DELETE wrap_original to /schema/*pk_pattern*

        Query Some One for /schema/_search
        List All  /schema/_list?start=0&count=10



    """

    METHOD_MAP = {'get': 'read', 'post': 'create',
                  'put': 'update', 'delete': 'delete'}

    api_route = [

    ]

    route2handler = {
        "read/write": ("POST", "GET"),
        "update/delete": ("PUT", "DELETE"),
        "list": ()

    }

    def __new__(mcs, name, bases, attributes):
        for http_method, instance_method in mcs.METHOD_MAP.items():
            if attributes.has_key(instance_method) and not attributes.has_key(http_method):
                attributes[http_method] = mcs.wrap_original(attributes[instance_method])
            elif attributes.has_key(http_method):
                attributes["orig_" + http_method] = attributes[http_method]
                attributes[http_method] = mcs.wrap_original(attributes[http_method])
        return type.__new__(mcs, name, bases, attributes)

    @classmethod
    def wrap_original(mcs, method):
        """
        return http request handling method
        :param method:
        :return:
        """

        def handle_request(*args, **kwargs):
            instance = args[0]
            try:
                instance.write_response(method(*args, **kwargs))
            except Exception, error:
                return instance.handler_error(error)

        @functools.wraps(method)
        def normal_wrapper(*args, **kwargs):
            instance = args[0]
            for mt in [mcs.logging_process(instance.prepare_request),
                       lambda: handle_request(*args, **kwargs),
                       mcs.logging_process(instance.finish_request)]:
                print instance, "Execute", mt
                mt()

        @tornado.gen.coroutine
        @functools.wraps(method)
        def generator_wrapper(*args, **kwargs):
            instance = args[0]
            mcs.logging_process(instance.prepare_request)
            for _ in method(*args, **kwargs):
                yield _
            mcs.logging_process(instance.finish_request)

        print "Register", method, inspect.isgeneratorfunction(method)
        if inspect.isgeneratorfunction(method):
            return generator_wrapper
        else:
            return normal_wrapper

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


class BaseHandler(tornado.web.RequestHandler):
    __metaclass__ = HandlerWrapper
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
        """
        load post json data
        :return:
        """
        self.request_obj = utils.DotDict(**json.loads(self.request.body))

    def write_response(self, obj, finish=True):
        self.response_string = json.dumps(obj)
        if not self._finished:
            self.write(self.response_string)
            if finish:
                self.finish()

    def finish_request(self):
        pass

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
        raise error


import http_codes


class BaseException(Exception):
    code = http_codes.INTERNAL_SERVER_ERROR  # default error
    msg = http_codes.code_message(code)

    def __init__(self, code=None, msg=None):
        if code:
            self.code = code
        self.msg = msg or self.msg or http_codes.code_message(self.code)
        super(BaseException, self).__init__(self.msg)
