#!/bin/sh
set -eu

cat << EOF > /etc/guacamole/guacamole.properties
guacd-hostname: ${GUACD_HOST:-localhost}
guacd-port: ${GUACD_PORT:-4822}
EOF

export GUACAMOLE_HOME=/etc/guacamole

exec jhsingle-native-proxy --debug --logs --authtype none --request-timeout 60 --ready-timeout 60 --progressive --destport 8080 -- java -jar $JETTY_HOME/start.jar --debug
# exec java -jar $JETTY_HOME/start.jar
