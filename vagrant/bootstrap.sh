#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get upgrade -y

# zeroconf hostnames
apt-get install -y \
    avahi-daemon

# mininet
apt-get install -y \
    python-pip \
    mininet \

pip install requests

# docker
apt-get get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

apt-get update

apt-get install -y \
    docker-ce \
    docker-compose \

