create:
	mkdir ../tr_vol
	mkdir ../tr_vol/database
	sudo docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up -d --build

up:
	sudo docker-compose --env-file srcs/.env -f srcs/docker-compose.yml up -d --build
	
restart:
	sudo docker-compose -f srcs/docker-compose.yml restart

stop:
	sudo docker-compose -f srcs/docker-compose.yml stop

down:
	sudo docker-compose -f srcs/docker-compose.yml down

clean: down
	sudo rm -rf ../tr_vol
	sudo docker volume rm srcs_database_vol
	sudo systemctl stop nginx

ps:
	sudo docker-compose -f srcs/docker-compose.yml ps

logs:
	sudo docker-compose -f srcs/docker-compose.yml logs

top:
	sudo docker-compose -f srcs/docker-compose.yml top

re:	clean create logs