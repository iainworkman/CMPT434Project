# basic apache server. To use either add or bind mount content under /var/www
FROM ubuntu:xenial

MAINTAINER Iain Workman <iain.workman@googlemail.com>

RUN apt-get --assume-yes update && \
		apt-get --assume-yes install build-essential ant maven python-dev \
																	openjdk-8-jdk git && \
		git clone git://github.com/floodlight/floodlight.git && \
		cd floodlight && \
		git submodule init && \
		git submodule update && \
		ant && \
		mkdir /var/lib/floodlight && \
		chmod 777 /var/lib/floodlight && \
		apt-get clean
RUN mkdir --parents /var/logs/floodlight && \
		echo \
			"cd floodlight && java -jar target/floodlight.jar > /var/logs/floodlight.log" > /run_floodlight.sh && \
		chmod +x /run_floodlight.sh
RUN touch /var/logs/floodlight.log

CMD /run_floodlight.sh 
