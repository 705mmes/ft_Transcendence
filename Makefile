create:
	mkdir ../tr_vol
	mkdir ../tr_vol/database
	sudo docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up -d --build --remove-orphans

prod:
	sudo docker-compose -f srcs/docker-compose.prod.yml up -d --build

up:
	sudo docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up -d --build --remove-orphans
	
restart:
	sudo docker-compose -f srcs/docker-compose.yml restart

stop:
	sudo docker-compose -f srcs/docker-compose.yml stop

down:
	sudo docker-compose -f srcs/docker-compose.yml down

clean: down
	-sudo docker-compose -f srcs/docker-compose.prod.yml down
	-sudo docker volume rm srcs_postgres_data
	-sudo docker network rm srcs_default
	-sudo rm -rf ../tr_vol
	-sudo systemctl stop nginx postgresql
	-sudo launchctl stop nginx postgresql

ps:
	sudo docker-compose -f srcs/docker-compose.yml ps

logs:
	sudo docker-compose -f srcs/docker-compose.yml logs

top:
	sudo docker-compose -f srcs/docker-compose.yml top

re:	clean create logs ps