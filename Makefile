.DEFAULT_GOAL := help

test:
	pytest -sv .

run:
	PYTHONPATH="src" python -m serve

run-docker:
	docker-compose up

start-test-mongo: ## start mongodb in docker for tests
	docker run -d --rm --name=fastapi_mongodb -p 27017:27017 --tmpfs=/data/db mongo

stop-test-mongo: ## stop dockerized mongodb for tests
	docker stop fastapi_mongodb

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
