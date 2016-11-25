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
    """Get request payload based on the
    request.method.
    """
    return {
        'GET': _get_url_params_as_dict,
        'POST': _get_request_body,
        'PUT': _get_request_body
    }[method]


def _get_url_params_as_dict(_request):
    """
    Get url query params as `dict`.
    """
    return _multi_dict_to_dict(_request.args)


def _get_request_body(_request):
    """
    Get the json payload of the request.
    """
    return _request.json


def _multi_dict_to_dict(_md):
    """Converts a `MultiDict` to a
    `dict` object.
    :param _md: object
    :type _md: MultiDict
    :returns: converted MultiDict object
    :rtype: dict
    """
    result = dict(_md)
    for key, value in result.items():
        if len(value) == 1:
            result[key] = serialize_number(value[0])
        else:
            result[key] = [serialize_number(v) for v in value]
    return result


def serialize_number(value):
    """
    Tries to convert `string` to `int`, if it can't -
    tries to convert to `float`, if it fails again -
    the `string` itself is returned.
    """
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
    """
    Read a .json file and return its content.
    """
    with open(path, 'r') as f:
        return json.load(f)


def validate_schema(payload, schema):
    """Validates the payload against a
    defined json schema for the requested
    endpoint.

    :param payload: incoming request data
    :type payload: dict
    :param schema: the schema the request payload should
                   be validated against
    :type schema: .json file
    :returns: errors if any
    :rtype: list
    """
    errors = []
    validator = jsonschema.Draft4Validator(schema,
                                           format_checker=jsonschema.FormatChecker())
    for error in sorted(validator.iter_errors(payload), key=str):
        errors.append(error.message)

    return errors


def _get_path_for_function(func):
    return os.path.dirname(os.path.realpath(inspect.getfile(func)))


def schema(path=None):
    """Validate the request payload with a JSONSchema.

    Decorator func that will be used to specify
    the path to the schema that the route/endpoint
    will be validated against.

    :param path: path to the schema file
    :type path: string
    :returns: list of errors if there are any
    :raises: InvalidAPIRequest if there are any errors

    ex:

    @schema('/path/to/schema.json')
    @app.route('/app-route')
    def app_route():
        ...
    """
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
