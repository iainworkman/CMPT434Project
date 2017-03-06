# basic apache server. To use either add or bind mount content under /var/www
FROM ubuntu:xenial

MAINTAINER Iain Workman <iain.workman@googlemail.com>

RUN apt-get --assume-yes update
RUN	apt-get --assume-yes install build-essential ant maven python-dev
RUN	apt-get --assume-yes install git
RUN git clone git://github.com/floodlight/floodlight.git
RUN cd floodlight
RUN git submodule init
RUN git submodule update
RUN ant
RUN mkdir /var/lib/floodlight
RUN chmod 777 /var/lib/floodlight
RUN apt-get clean

CMD ["java","-jar","target/floodlight.jar"]
