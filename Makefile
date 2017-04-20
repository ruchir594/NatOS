QUEUE_SERVER=./queue-server
all:
	add-apt-repository ppa:chris-lea/redis-server
	apt-get update
	apt-get install redis-server
	pip install -r requirements.txt
	service redis-server start
	nohup $(which) python $(QUEUE_SERVER) & # doesn't works when you reboot, TODO - make service

