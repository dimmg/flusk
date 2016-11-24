import inspect
import json
import os
from functools import wraps

from flask import request
import jsonschema

from .exceptions import InvalidAPIRequest

SCHEMAS_DIR = 'core/api/specifications/schemas'
SCHEMAS_PATH = os.path.join(os.getcwd(), SCHEMAS_DIR)


def get_request_payload(method):
    return {
        'GET': _get_url_params_as_dict,
        'POST': _get_request_body,
        'PUT': _get_request_body
    }[method]


def _get_url_params_as_dict(_request):
    return _multi_dict_to_dict(_request.args)


def _get_request_body(_request):
    return _request.json


def _multi_dict_to_dict(_md):
    result = dict(_md)
    for key, value in result.items():
        if len(value) == 1:
            result[key] = serialize_number(value[0])
        else:
            result[key] = [serialize_number(v) for v in value]
    return result


def serialize_number(value):
    try:
        _val = int(value)
    except ValueError:
        pass
    try:
        _val = float(value)
    except ValueError:
        return value
    return _val


def get_schema(path):
    with open(path, 'r') as f:
        return json.load(f)


def validate_schema(payload, schema):
    errors = []
    validator = jsonschema.Draft4Validator(schema,
                                           format_checker=jsonschema.FormatChecker())
    for error in sorted(validator.iter_errors(payload), key=str):
        errors.append(error.message)

    return errors


def _get_path_for_function(func):
    return os.path.dirname(os.path.realpath(inspect.getfile(func)))


def schema(path=None):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            _path = path.lstrip('/')
            schema_path = os.path.join(SCHEMAS_PATH, request.blueprint, _path)
            payload = get_request_payload(request.method)(request)

            errors = validate_schema(payload, get_schema(schema_path))
            if errors:
                raise InvalidAPIRequest(message=errors)

            return func(*args, **kwargs)
        return wrapped
    return decorator
