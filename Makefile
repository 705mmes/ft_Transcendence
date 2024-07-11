build:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up -d --build
	
up:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up -d

prod:
	docker-compose -f srcs/docker-compose.prod.yml up --build

prud:
	docker-compose -f srcs/docker-compose.prod.yml up
	
restart:
	docker-compose -f srcs/docker-compose.prod.yml restart

stop:
	docker-compose -f srcs/docker-compose.prod.yml stop

down:
	docker-compose -f srcs/docker-compose.prod.yml down

clean: down
	- docker volume rm srcs_postgres_data srcs_pgadmin_data srcs_static_volume
	- systemctl stop nginx postgresql
	- launchctl stop nginx postgresql

ps:
	docker-compose -f srcs/docker-compose.prod.yml ps

logs:
	docker-compose -f srcs/docker-compose.prod.yml logs

top:
	docker-compose -f srcs/docker-compose.prod.yml top

fclean: clean
	docker system prune -af

re:	clean up logs ps