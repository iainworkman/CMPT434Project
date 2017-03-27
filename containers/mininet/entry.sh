#!/bin/sh

set -eu

service openvswitch-switch start

floodlight_is_up() {
    local url="http://${FL_HOST:-localhost}:${FL_PORT:-8080}"
    curl -s "${url}" > /dev/null
}

until floodlight_is_up ; do
    >&2 echo "floodlight is down - sleeping"
    sleep 1
done

>&2 echo "floodlight is up - starting mininet"
if [ -e $1 ]; then
    exec python $@
else
    exec sh
    >&2 echo "file $1 does not exist"
    exit 1
fi

