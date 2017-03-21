#! /bin/bash

service openvswitch-switch start

cd floodlight
nohup java -jar target/floodlight.jar &
sleep 5s
python -E /clone_network.py 127.0.0.1 8080 127.0.0.1 6663

