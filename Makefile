# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)


TARGET_MAX_CHAR_NUM=20
## show help
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo ''

## starts docker compose(db+container) in background mode
start:
	docker-compose up -d
	docker-compose restart sendcloud_web
	docker-compose ps

## stops docker-compose (not 'down' docker-compose)
stop:
	docker-compose stop

## build and start docker-compose, apply migrations
init:
	docker-compose down
	docker-compose build
	make start
	sleep 5
	make migrate

## create migrations files for the Django
migrations:
	docker-compose exec sendcloud_web python /code/manage.py makemigrations

## apply migrations for the Django
migrate:
	docker-compose exec sendcloud_web python /code/manage.py migrate

## open Django shell
shell:
	docker-compose exec sendcloud_web python /code/manage.py shell

## open Django bash
bash:
	docker-compose exec sendcloud_web bash

## change owner to current user for all files in the project
chown:
	sudo chown -R ${USER}:${USER} .

## delete database
dropdb:
	docker-compose stop sendcloud_db_service
	docker-compose rm -vf sendcloud_db_service

## drop db -> recreate db -> run migrations
restart_db:
	make stop
	docker-compose rm -vf sendcloud_db_service
	make start
	make migrate


## run tests. Args: optional <path> to tests in the project directory
test:
	docker-compose exec sendcloud_web pytest -s /code/${path}

## dump all data from the DB. Output - "db.json" file
dump_all:
	docker-compose exec sendcloud_web python /code/manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude admin --exclude sessions > fixtures/db.json

## load data from the DB dump file
load_data:
	docker-compose exec sendcloud_web python /code/manage.py loaddata fixtures/db.json
