.PHONY: usage start stop restart inspect log stopall tests cli requirements clean deploy


# Colors
NC=\x1b[0m
L_GREEN=\x1b[32;01m

## usage: print useful commands
usage:
	@echo "$(L_GREEN)Choose a command: $(PWD) $(NC)"
	@bash -c "sed -ne 's/^##//p' ./Makefile | column -t -s ':' |  sed -e 's/^/ /'"

## start: starts web server and db using docker-compose up
start:
	docker-compose up -d web

## start: starts web server and db using docker-compose down
stop:
	docker-compose down

## rebuild: rebuilds container
rebuild:
	docker stop recordbin-web
	docker-compose up -d --build web

## restart: stops and starts all services
restart:
	stop & start

## inspect: opens a bash into the running web container using docker exec
inspect:
	docker exec -it recordbin-web bash

## inspectsb: similar to inspect but calls 'psql' into container db
inspectdb:
	psql -p 5433 -U postgres -d recordbindb -h 0.0.0.0

## inspectshell: similar to inspect but calls 'manage.py shell'
inspectshell:
	docker exec -it recordbin-web python manage.py shell

## log: opens the running web service using docker attach
log:
	docker attach recordbin-web

## stopall: kills all running docker web containers
stopall:
	docker ps | grep "recordbin-web" | awk '{print $$1}' | xargs docker stop

## tests: run test suite (alows pdb and breakpoint)
tests:
	docker-compose run --service-ports --rm tests
	docker stop recordbin-web
	docker stop postgres_test_db

## testsbash: runs bash inside test container for easier test troubleshooting
testsbash:
	docker-compose up -d tests
	docker exec -it recordbin-test bash

## format: Format code using black
format:
	docker-compose run --rm --no-deps web bash -c "black backend --exclude .+migrations & black tests"

## lint: Runs flake8
lint:
	docker-compose run --rm --no-deps web bash -c "flake8"

## ci: run test suite
requirements:
	pipenv lock --requirements > requirements.txt

## clean: delete python artifacts
clean:
	python3 -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	python3 -c "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

## clean: delete python artifacts
deploy:
	heroku container:login
	heroku container:push web --app recordbin-api
	heroku container:release web --app recordbin-api
