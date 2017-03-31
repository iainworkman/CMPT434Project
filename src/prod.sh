#!/bin/bash
sudo mn -c &> /dev/null
sudo mn --custom production_topology.py --topo demo --controller remote,port=6653
