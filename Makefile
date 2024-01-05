VOL_DIR	= ${HOME}/data

NEEDS_LIB = login game matchmaking users

all: commons
	[ -d $(VOL_DIR)/mysql ] || mkdir -p $(VOL_DIR)/mysql
	docker-compose --env-file ./srcs/.env -f ./srcs/docker-compose.yml up -d

build:
	docker-compose -f ./srcs/docker-compose.yml --env-file ./srcs/.env build --no-cache

stop:
	docker stop $(shell docker ps -qa)

clean: 
	docker stop $(shell docker ps -qa); docker rm $(shell docker ps -qa) ; docker rmi -f $(shell docker images -qa); docker volume rm $(shell docker volume ls -q); docker network rm $(shell docker network ls -q) 2>/dev/null

prune:
	docker system prune --all
	docker volume prune

re:
	docker-compose -f ./srcs/docker-compose.yml up --force-recreate --no-deps -d

commons:
	cd srcs/ && python setup.py sdist bdist_wheel && pip install --force-reinstall dist/tcommons-1.0.0-py3-none-any.whl

build-commons:
	cd srcs/ && python setup.py sdist bdist_wheel

# Services that need commons
game login matchmaking users: build-commons
	mv srcs/dist/tcommons-1.0.0-py3-none-any.whl srcs/$@
	docker-compose -f ./srcs/docker-compose.yml up -d $@

# Services that don't need commons
front database endpoint:
	docker-compose -f ./srcs/docker-compose.yml up -d $@

db:
	docker-compose -f ./srcs/docker-compose.yml up -d database

hakim:
	docker-compose -f ./srcs/docker-compose.yml up --build database redis users login notifications

.PHONY: clean re stop build db all 
