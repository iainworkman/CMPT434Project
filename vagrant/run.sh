#!/usr/bin/env bash

cd /vagrant/production_network
docker-compose up -d

sleep 1

cd /vagrant/clone_network
docker-compose up -d

