#! /bin/bash

service openvswitch-switch start

cd floodlight
nohup java -jar target/floodlight.jar &
sleep 1s
python -E /production_network.py

