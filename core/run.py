import os

from werkzeug.contrib.fixers import ProxyFix

from api import create_app


app = create_app()

def run():
    debug = os.environ.get('APP_DEBUG', True)
    host = os.environ.get('APP_HOST', '0.0.0.0')
    port = int(os.environ.get('APP_PORT', 5000))

    app.run(debug=debug, host=host, port=port)


wsgi = ProxyFix(app.wsgi_app)


if __name__ == '__main__':
    run()
