#!/bin/sh
set -eu

LOCALHOST=${LOCALHOST:-yes}

if [ "$LOCALHOST" = "yes" ]; then
  LOCALHOST_ARGS="-localhost yes"
elif [ "$LOCALHOST" = "no" ]; then
  LOCALHOST_ARGS="-localhost no --I-KNOW-THIS-IS-INSECURE"
else
  echo "Error: LOCALHOST environment variable must be set to 'yes' or 'no'"
  exit 1
fi

if [ ! -d /home/ubuntu/Desktop ]; then
  echo "First run, setting up ubuntu"
  rsync /home/ubuntu.orig/ -av --ignore-existing /home/ubuntu/
fi

/usr/bin/tigervncserver :1 -fg $LOCALHOST_ARGS -SecurityTypes None -xstartup /usr/local/bin/start-mate.sh
