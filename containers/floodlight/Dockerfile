FROM ubuntu:xenial

MAINTAINER Jarrod Pas <docker@jarrodpas.com>

RUN apt-get update \
 && apt-get install -y \
            ant \
            build-essential \
            git \
            maven \
            openjdk-8-jdk \
            python-dev

RUN git clone git://github.com/floodlight/floodlight.git \
 && cd floodlight \
 && git submodule init \
 && git submodule update \
 && ant \
 && mkdir -p /var/lib/floodlight

COPY entry.sh /entry.sh

ENTRYPOINT /entry.sh

