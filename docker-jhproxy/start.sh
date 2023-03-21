#!/bin/sh
set -eu

if [ $# -lt 1 ]; then
  echo "Expected argument HOST:PORT"
  exit 1
fi
HOST_PORT="$1"

jhsingle-native-proxy --debug --logs --authtype none --request-timeout 15 -- socat TCP-LISTEN:{port},fork,reuseaddr "TCP:$HOST_PORT"
