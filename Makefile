build:
	sudo docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up -d --build
	
up:
	sudo docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up -d

prod:
	sudo docker-compose -f srcs/docker-compose.prod.yml up --build

prud:
	sudo docker-compose -f srcs/docker-compose.prod.yml up
	
restart:
	sudo docker-compose -f srcs/docker-compose.prod.yml restart

stop:
	sudo docker-compose -f srcs/docker-compose.prod.yml stop

down:
	sudo docker-compose -f srcs/docker-compose.prod.yml down

clean: down
	-sudo docker volume rm srcs_postgres_data srcs_pgadmin_data srcs_static_volume
	-sudo systemctl stop nginx postgresql
	-sudo launchctl stop nginx postgresql

ps:
	sudo docker-compose -f srcs/docker-compose.prod.yml ps

logs:
	sudo docker-compose -f srcs/docker-compose.prod.yml logs

top:
	sudo docker-compose -f srcs/docker-compose.prod.yml top

fclean: clean
	sudo docker system prune -af

re:	clean up logs ps