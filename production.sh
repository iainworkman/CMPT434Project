#!/bin/bash

controller_host='floodlight.local'
controller_port='6653'

set -eu

if ! [ $(id -u) = 0 ]; then
    >&2 echo "mininet must be run as root"
    exit 1
fi

getip() {
    ping -c 1 ${1} | awk -F '[ :]' 'NR==2 { print $4 }'
}

controller_ip=$(getip ${controller_host})

cd src

mn -c &> /dev/null
mn --custom production_topology.py \
   --topo demo \
   --controller "remote,ip=${controller_ip},port=${controller_port}"

