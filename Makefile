build:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up --build
	
up:
	docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up

restart:
	docker-compose -f srcs/docker-compose.yml restart

stop:
	docker-compose -f srcs/docker-compose.yml stop

down:
	docker-compose -f srcs/docker-compose.yml down

clean: down
	- docker volume rm srcs_postgres_data srcs_pgadmin_data srcs_static_volume
	# - systemctl stop nginx postgresql
	# - launchctl stop nginx postgresql

ps:
	docker-compose -f srcs/docker-compose.yml ps

logs:
	docker-compose -f srcs/docker-compose.yml logs

top:
	docker-compose -f srcs/docker-compose.yml top

fclean: clean
	docker system prune -af

re:	clean up logs ps