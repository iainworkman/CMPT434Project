#!/bin/bash

set -e

docker-compose up -d
docker attach clone_net
