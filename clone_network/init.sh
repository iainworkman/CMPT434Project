#! /bin/bash

service openvswitch-switch start

cd floodlight
nohup java -jar target/floodlight.jar > /floodlight.log &
sleep 5s
mn -c && \
python -E /clone_network.py 172.16.1.69 8080 127.0.0.1 6653

