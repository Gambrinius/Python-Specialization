import json
import functools


def to_json(func):

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        value = func(*args, **kwargs)
        serialized_value = json.dumps(value)
        return serialized_value

    return wrapped
