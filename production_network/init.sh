#! /bin/bash

service openvswitch-switch start

cd floodlight
nohup java -jar target/floodlight.jar &
sleep 1s
mn -c && \
python -E /production_network.py

