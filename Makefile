build:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up --build

prod:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.prod.yml up --build
	
up:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up

prud:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.prod.yml up

down:
	docker-compose -f srcs/docker-compose.yml down --remove-orphans -v --rmi all

pdown:
	docker-compose -f srcs/docker-compose.prod.yml down --remove-orphans -v --rmi all

ps:
	docker-compose -f srcs/docker-compose.yml ps

pps:
	docker-compose -f srcs/docker-compose.prod.yml ps

prune:
	docker system prune -af