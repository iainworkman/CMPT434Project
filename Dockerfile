# Floodlight Docker Image which builds from the master branch
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
RUN apt-get --assume-yes install net-tools mininet && \
		apt-get clean
RUN apt-get install -y python-setuptools && \
		git clone git://github.com/kennethreitz/requests.git && \
		cd requests && \
		python setup.py install
CMD /init.sh 
