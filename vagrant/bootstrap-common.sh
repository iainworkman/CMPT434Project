#!/usr/bin/env bash

sed -i 's|http://.*archive.ubuntu.com|http://mirror.csclub.uwaterloo.ca|' /etc/apt/sources.list

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get upgrade -y

# zeroconf hostnames
apt-get install -y \
    avahi-daemon

