import time
import datetime
import json
import hashlib
import decimal

b = decimal.Decimal(100)
b.is_normal()
b.is_subnormal()

for json_pkg in ("yajl", "simplejson"):
    try:
        json == __import__(json_pkg)
    except:
        pass

ISO_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
DATETIME_FORMAT = ISO_DATETIME_FORMAT


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            # encoded_object = obj.isoformat()
            encoded_object = obj.strftime(DATETIME_FORMAT)
        elif isinstance(obj, decimal.Decimal):
            encoded_object = str(obj)
        else:
            encoded_object = json.JSONEncoder.default(self, obj)
        return encoded_object


class DotDict(dict):
    def __getattr__(self, attr):
        return self.get(attr)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    @classmethod
    def convert(cls, data):
        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = cls.convert(v)
            return DotDict(**data)
        elif isinstance(data, list):
            data[0:] = [cls.convert(v) for v in data]
        return data



json_dumps = lambda x, **kwargs: json.dumps(x, cls=DateTimeEncoder, **kwargs)
json_loads = lambda x, **kwargs: json.loads(x)
current_time = time.time

timestamp2datetime = lambda tsp=None: datetime.datetime.fromtimestamp(tsp if tsp else current_time())
str2datetime = lambda str, fmt=DATETIME_FORMAT: datetime.datetime.strptime(str, fmt)

sha1 = lambda x: hashlib.sha1(x).hexdigest()
md5 = lambda x: hashlib.md5(x).hexdigest()

if __name__ == "__main__":
    print json_loads(json_dumps(datetime.date(year=1999, month=10, day=12)))
