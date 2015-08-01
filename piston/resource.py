import tornado.web
import tornado.gen
import functools
import copy


class RestFulApiGenerator(type):
    method_map = {'get': 'read', 'post': 'create',
                  'put': 'update', 'delete': 'remove'}

    api_route = [

    ]

    """ automatically generate api route

        GET & POST mapping to /schema
        PUT & DELETE mapping to /schema/*primarykey_pattern*

        Query Some One for /schema/_search
        List All  /schema/_list?start=0&count=10



    """

    method2route_pattern = {
        "GET":"",
        "POST":"",


    }

    api_prefix = ''

    def __new__(mcs, name, bases, attributes):
        print name, bases, attributes
        resource_name = attributes.get("resource_name") or name
        primary_key_format = attributes.get("primary_key_format") or "(\w+)"
        route = mcs.format_route_path(resource_name, primary_key_format)
        added_methods = {}
        for origin_method, data_opt in mcs.method_map.items():
            added_methods[origin_method] = mcs.processing(attributes[data_opt])
        # mcs.add_handler_to_route()
        attributes.update(added_methods)
        return type.__new__(mcs, name, bases, attributes)

    @staticmethod
    def processing(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            instance = args[0]
            try:
                instance.prepare_request(*args, **kwargs)
            except Exception, e:
                pass
            try:
                return method(*args, **kwargs)
            except Exception, error:
                return args[0].error_handle(error)

        return wrapper

    @classmethod
    def building_api(mcs, name, bases, attributes, methods):
        pass

    @classmethod
    def format_route_path(mcs, resource_name, primary_key_format, path_type=""):
        return '/'.join((mcs.api_prefix, resource_name, primary_key_format))

    @classmethod
    def add_handler_to_route(mcs, handler, route):
        mcs.api_route.append((route, handler))


class Resource(tornado.web.RequestHandler):
    __metaclass__ = RestFulApiGenerator
    sub_resources = ()
    resource_name = None
    primary_key_format = "(\w+)"

    def prepare_request(self):
        pass

    def auth(self):
        pass

    def initialize(self):
        pass

    def read(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def remove(self):
        pass

    def query(self):
        pass

    def list_all(self):
        pass

    def error_handle(self, error):
        pass

    def build_response(self):
        pass
