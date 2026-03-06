app_name = simple_task_manager

docker_compose := docker compose -f docker-compose.yml

build:
	$(docker_compose) build $(c)

rebuild:
	$(docker_compose) up -d --build --force-recreate $(c)
	docker image prune -f
up:
	$(docker_compose) up -d $(c)

start:
	$(docker_compose) start $(c)

down:
	$(docker_compose) down $(c)

reup:
	$(docker_compose) down $(c)
	$(docker_compose) up -d $(c)

destroy:
	$(docker_compose) down --rmi all -v $(c)

stop:
	$(docker_compose) stop $(c)

restart:
	$(docker_compose) restart $(c)

logs:
	$(docker_compose) logs --tail=1000 -f $(c)

app-logs:
	$(docker_compose) logs --tail=1000 -f backend $(c)

app-bash:
	docker exec -it $(app_name)_backend bash $(c)

db-bash:
	docker exec -it $(app_name)_postgres bash $(c)

psql:
	docker exec -it $(app_name)_postgres psql -U postgres

#Alembic

alembic:
	docker exec -it $(app_name)_backend alembic $(c)

autogenerate:
	docker exec -it $(app_name)_backend alembic revision --autogenerate -m "$(m)"

upgrade:
	docker exec -it $(app_name)_backend alembic upgrade head

downgrade:
	docker exec -it $(app_name)_backend alembic downgrade -1

alembic-current:
	docker exec -it $(app_name)_backend alembic current

alembic-history:
	docker exec -it $(app_name)_backend alembic history
