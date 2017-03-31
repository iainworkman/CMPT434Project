#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive
apt-get update

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

usermod -aG docker vagrant

curl -L "https://github.com/docker/compose/releases/download/1.11.2/docker-compose-$(uname -s)-$(uname -m)" \
     -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose

