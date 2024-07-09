up:
	sudo docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up -d --build

prod:
	sudo docker-compose -f srcs/docker-compose.prod.yml up -d --build
	
restart:
	sudo docker-compose -f srcs/docker-compose.prod.yml restart

stop:
	sudo docker-compose -f srcs/docker-compose.prod.yml stop

down:
	sudo docker-compose -f srcs/docker-compose.prod.yml down

clean: down
	-sudo docker volume rm srcs_postgres_data srcs_pgadmin_data srcs_static_volume
	-sudo rm -rf ../tr_vol
	-sudo systemctl stop nginx postgresql
	-sudo launchctl stop nginx postgresql

ps:
	sudo docker-compose -f srcs/docker-compose.prod.yml ps

logs:
	sudo docker-compose -f srcs/docker-compose.prod.yml logs

top:
	sudo docker-compose -f srcs/docker-compose.prod.yml top

re:	clean up logs ps