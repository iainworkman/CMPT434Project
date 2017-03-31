#!/bin/bash
prod_ip=${1:-10.0.2.4}
prod_port=8080
clone_ip=$prod_ip
clone_port=6654

sudo mn -c &> /dev/null
sudo -E python clone_network.py $prod_ip $prod_port $clone_ip $clone_port
