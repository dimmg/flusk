import json
from functools import singledispatch

from flask import jsonify, Response, request
from werkzeug.exceptions import NotFound

from ..exceptions import JSONException, InvalidAPIRequest


@singledispatch
def to_serializable(rv):
    pass


@to_serializable.register(dict)
def ts_dict(rv):
    return jsonify(rv)


@to_serializable.register(list)
def ts_list(rv):
    return Response(json.dumps(rv, indent=4, sort_keys=True))


class JSONResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        rv = to_serializable(rv)
        return super(JSONResponse, cls).force_type(rv, environ)


def json_error_handler(app):
    @app.errorhandler(JSONException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response


    @app.errorhandler(NotFound.code)
    def resource_not_found(error):
        msg = 'The requested URL `%s` was not found on the server.' % request.path
        response = jsonify(InvalidAPIRequest(message=msg).to_dict())
        response.status_code = NotFound.code
        return response
