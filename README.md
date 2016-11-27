# Flusk

Flask - SQLAlchemy's declarative base - Docker - custom middleware.

## Specifications

##### Application factory

Factories helps in creating many instances of the application.
In this project, testing environment creates a new app instance whenever tests are ran.

[Read More](http://flask.pocoo.org/docs/0.11/patterns/appfactories/)

##### Blueprints

Blueprints helps to split large application in small modular packages (one would say - similar to `django apps`).

[Read More](http://flask.pocoo.org/docs/0.11/blueprints/#blueprints)

##### Logic separation

The logic is splitted in the following layers:

- `backend` (persistence layer) - where resides the code to read/write/delete records to disk or database
- `domain` (domain layer) - where resides the bussines logic and external api integrations, i/o operations for a blueprint
- `views` (presentation layer) - knows only about HTTP `request` and `response`. Its duty is to process a request and pass data to lower layers and to return responses.
- `models` (data model layer) - where all blueprint models are defined

##### Middleware

The application tends to use middlewares instead of decorators or custom functions across the project.

- **application/json requests** - ensures that all incoming requests are of `application/json` Content-Type
- **schema validation** - validates the request payload against a JSON Schema
- **cors** - allow cors requests for consumer apps
- **json exceptions** - custom exception handler used to raise JSON exceptions
- **json responses** - custom response handler used to return JSON objects

##### Extensions

The project tends to use the framework agnostic extensions over the flask ones, because they are usually wrappers and besides that, they may add additional functionality that you don't actually need (e.g. managers)

##### Docker

Ensures that the application you develop on local machine, behaves exactly in production.

[Official Site](https://www.docker.com/)

## Directory layout

```
.
├── core                                   # main codebase for the application
│   ├── api                                # API specific codebase
│   │   ├── common                         # shared logic used by the application
│   │   │   ├── database.py                # common database logic
│   │   │   ├── exceptions.py              # custom exception classes
│   │   │   ├── __init__.py
│   │   │   ├── middleware                 # application middleware
│   │   │   │   ├── __init__.py            # define application middlewares
│   │   │   │   ├── request.py             # `request` related middleware
│   │   │   │   └── response.py            # `response` related middleware
│   │   │   ├── serializers.py             # custom defined serializers
│   │   │   └── validation.py              # JSON schema validation logic
│   │   ├── conftest.py                    # pytest configurations and custom fixtures
│   │   ├── foss                           # flask blueprint
│   │   │   ├── backend.py                 # logic related to database queries
│   │   │   ├── domain.py                  # business logic and external integrations
│   │   │   ├── __init__.py                # blueprint config
│   │   │   ├── models.py                  # blueprint models
│   │   │   ├── tests                      # blueprint tests
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_unit.py           # unit tests
│   │   │   │   ├── test_integration.py    # integration tests
│   │   │   │   └── test_models.py         # database models tests
│   │   │   └── views.py                   # logic related to request -> response
│   │   ├── __init__.py                    # app factory, blueprints, errorhandler and middleware registration
│   │   └── specifications                 # API specifications, RAML files and JSON schemas
│   │       └── schemas                    # JSON schemas folder
│   │           └── foss                   # schemas for a specific blueprint
│   │               ├── create_foss.json   # endpoint/view/route schema
│   │               └── update_foss.json   # endpoint/view/route schema
│   ├── Dockerfile                         # Dockerfile for the flask application
│   ├── requirements.txt                   # application dependencies
│   └── run.py                             # application creation and running
├── docker-compose.yml                     # Dockerfiles manager
├── Makefile                               # set of useful tasks (make `targets`)
├── nginx                                  # nginx docker image related information
│   ├── Dockerfile                         # Dockerfile for the nginx web server
│   └── sites-enabled
│       └── nginx.conf                     # nginx configuration
└── README.md
```

## Prerequisites

- Python 3.5
- Docker

## Installation


#### Clone the repository

```
git clone https://github.com/dimmg/flusk.git
```

#### Build and run docker images

```
make dcompose-start
```

#### Run application

- ##### Development

    SSH into the running `api` container and start the development server

    ```
    docker exec -it flusk_api_1 bash
    python run.py
    ```

    By having a running server, execute

    ```
    docker inspect rbms_nginx_1
    ```

    where `IPAddress` it is the address of the running application.



- ##### Production

    Change `docker-compose.yml` file as follows:

    ```
    command:
        gunicorn -w 1 -b 0.0.0.0:5000 run:wsgi
        # tail -f /dev/null
    ```

    Rebuild the images via

    ```
    make dcompose-restart
    ```

    After rebuilding, the `gunicorn` wsgi server is running in background.

    To get the address of the running web server container run

    ```
    docker inspect rbms_nginx_1
    ```

#### Migrations

Migrations are done using the `alembic` migration tool.

##### Flow

1. make changes to your models when needed
2. create a migration
3. check the migration script and modify it as needed
4. apply the migration

##### Commands

- create migration
```
make db-revision msg=<..message..>
```

- apply the last migration
```
make db-upgrade
```

- get the raw SQL for the last migration
```
make db-upgrade-sql
```

Note that these are the basic migration commands. To get the most from alembic, use the original `$ alembic` runner.





