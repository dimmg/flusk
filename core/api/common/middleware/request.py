import os

from flask import current_app, request
from sqlalchemy.exc import DatabaseError

from ..database import db_session
from ..exceptions import InvalidContentType, InvalidPermissions


def ensure_content_type():
    content_type = request.headers.get('Content-type')
    if not content_type == 'application/json':
        raise InvalidContentType(
            message='Invalid content-type. Only `application-json` is allowed.'
        )


def ensure_public_unavailability():
    if not request.headers.get('_secure_key', '') == os.environ.get('SECURE_API_KEY'):
        raise InvalidPermissions(
            message='You don\'t have enough permissions to perform this action.'
        )


ACL_ORIGIN = 'Access-Control-Allow-Origin'
ACL_METHODS = 'Access-Control-Allow-Methods'
ACL_ALLOWED_HEADERS = 'Access-Control-Allow-Headers'

OPTIONS_METHOD = 'OPTIONS'
ALLOWED_ORIGINS = 'http://localhost:8080'
ALLOWED_METHODS = 'GET, POST, PUT, DELETE, OPTIONS'
ALLOWED_HEADERS = 'Authorization, DNT, X-CustomHeader, Keep-Alive, User-Agent, ' \
                  'X-Requested-With, If-Modified-Since, Cache-Control, Content-Type'


def enable_cors(response):
    if request.method == OPTIONS_METHOD:
        response = current_app.make_default_options_response()
    response.headers[ACL_ORIGIN] = ALLOWED_ORIGINS
    response.headers[ACL_METHODS] = ALLOWED_METHODS
    response.headers[ACL_ALLOWED_HEADERS] = ALLOWED_HEADERS

    return response


def commit_session(response):
    if response.status_code >= 400:
        return response
    try:
        db_session.commit()
    except DatabaseError:
        db_session.rollback()
    return response


def shutdown_session(exception=None):
    db_session.remove()
