build:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up --build

prod:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.prod.yml up --build
	
up:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up

prud:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.prod.yml up

down:
	docker-compose -f srcs/docker-compose.yml down

pdown:
	docker-compose -f srcs/docker-compose.prod.yml down

ps:
	docker-compose -f srcs/docker-compose.yml ps

pps:
	docker-compose -f srcs/docker-compose.prod.yml ps

clean: down pdown
	- docker volume rm srcs_postgres_data srcs_pgadmin_data srcs_static_volume

fclean: clean
	docker system prune -af