from flask import Flask

from .common.database import init_db
from .common.middleware import after_request_middleware, before_request_middleware, teardown_appcontext_middleware
from .common.middleware import response
from .foss import bp as foss_bp


def create_app():
    # initialize flask application
    app = Flask(__name__)

    # register all blueprints
    app.register_blueprint(foss_bp)

    # register custom response class
    app.response_class = response.JSONResponse

    # register before request middleware
    before_request_middleware(app=app)

    # register after request middleware
    after_request_middleware(app=app)

    # register after app context teardown middleware
    teardown_appcontext_middleware(app=app)

    # register custom error handler
    response.json_error_handler(app=app)

    # initialize the database
    init_db()

    return app
