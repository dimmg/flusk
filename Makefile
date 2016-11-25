ENV_FILE = $(shell pwd)$(shell echo '/core/.env')

include $(ENV_FILE)
export $(shell sed 's/=.*//' `pwd`/core/.env)

_DEVELOPMENT_DATABASE_URI=$(DEVELOPMENT_DATABASE_URI)
_TEST_DATABASE_URI=$(TEST_DATABASE_URI)

.PHONY: clear run-server run-tests help dcompose-start dcompose-start dcompose-stop dcleanup

clear:
	@find . -name __pycache__ -prune -exec rm -rf {} +
	@find . -name "*.pyc" -prune -exec rm -rf {} +
	@find . -name .cache -prune -exec rm -rf {} +

dcompose-start:
	@docker-compose stop;
	@docker-compose build;
	@docker-compose up -d;

dcompose-restart:
	@docker-compose stop;
	@docker-compose build;
	@docker-compose up -d;

dcompose-stop:
	@docker-compose stop

dcleanup:
	@docker rm $(shell docker ps -qa --no-trunc --filter "status=exited")
	@docker rmi $(shell docker images --filter "dangling=true" -q --no-trunc)

run-server:
	@(\
		export SQLALCHEMY_DATABASE_URI=$(_DEVELOPMENT_DATABASE_URI); \
		python ./core/run.py; \
	)

run-tests: clear
	@(\
		export SQLALCHEMY_DATABASE_URI=$(_TEST_DATABASE_URI); \
		pytest -s; \
	)

help:
	@echo 'dcompose-start:'
	@echo '	Build and start containers'
	@echo 'dcompose-stop:'
	@echo '	Stop running containers'
	@echo 'dcleanup:'
	@echo '	Remove docker containers with status `exited`'
	@echo '	Remove unused docker images'
	@echo 'run-server:'
	@echo '	Start application server'
	@echo 'run-tests:'
	@echo '	Run tests'
	@echo 'clear':
	@echo '	Remove *.pyc files, __pycache__ and .cache folders'

