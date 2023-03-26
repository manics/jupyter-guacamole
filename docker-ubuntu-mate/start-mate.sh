#!/bin/sh

# Firefox sandboxing may not work in a container
# https://wiki.mozilla.org/Security/Sandbox#Environment_variables
export MOZ_DISABLE_CONTENT_SANDBOX=1
export MOZ_DISABLE_GMP_SANDBOX=1
export MOZ_DISABLE_RDD_SANDBOX=1
export MOZ_DISABLE_SOCKET_PROCESS_SANDBOX=1

exec dbus-launch mate-session "$@"
