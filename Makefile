QUEUE_SERVER=./queue-server
INITD_FILE=/etc/init.d/queue-server
all:
	wget http://download.redis.io/redis-stable.tar.gz
	tar xvzf redis-stable.tar.gz
	cd redis-stable
	make
	cd src
	sudo cp redis-server /usr/local/bin
	sudo cp redis-cli /usr/local/bin
	cd ..
	cd ..
	rm redis-stable.tar.gz
	cd redis-stable
	sudo mkdir /etc/redis
	sudo mkdir /var/redis
	sudo cp utils/redis_init_script /etc/init.d/redis_6379
	sudo cp redis.conf /etc/redis/6379.conf
	sudo mkdir /var/redis/6379
	cd ..
	apt-get update
	apt-get install redis-server
	pip install -r requirements.txt
	touch $(INITD_FILE)
	printf "\nservice redis-server start\nnohup $(which python) $PWD/queue-server.py &\n" >> $(INITD_FILE)
	service redis-server start
	nohup $(which) python $(QUEUE_SERVER) &
