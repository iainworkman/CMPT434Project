#!/bin/sh

set -eu

FL_HOST=${1}
FL_PORT=8080
shift

service openvswitch-switch start

floodlight_is_up() {
    local url="http://${FL_HOST:-localhost}:${FL_PORT:-8080}"
    curl -s "${url}" > /dev/null
}

until floodlight_is_up ; do
    >&2 echo "floodlight (${FL_HOST}) is down - sleeping"
    sleep 1
done

>&2 echo "floodlight is up - running command"
exec $@

