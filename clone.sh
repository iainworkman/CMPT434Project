#!/bin/bash

production_control_host='floodlight.local'
production_control_port=8080

clone_control_host='floodlight.local'
clone_control_port='6654'

if ! [ $(id -u) = 0 ]; then
    >&2 echo "mininet must be run as root"
    exit 1
fi

getip() {
    ping -c 1 ${1} | awk -F '[ :]' 'NR==2 { print $4 }'
}

production_control_ip=$(getip ${production_control_host})
clone_control_ip=$(getip ${clone_control_host})

cd src

mn -c &> /dev/null
python clone_network.py \
        ${production_control_ip} \
        ${production_control_port} \
        ${clone_control_ip} \
        ${clone_control_port}

