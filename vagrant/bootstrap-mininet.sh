#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive
apt-get update

# mininet
apt-get install -y \
    python-pip \
    mininet \

pip install requests

