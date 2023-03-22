#!/bin/sh
set -eu

cat << EOF > /etc/guacamole/guacamole.properties
guacd-hostname: ${GUACD_HOST:-localhost}
guacd-port: ${GUACD_PORT:-4822}
EOF

export GUACAMOLE_HOME=/etc/guacamole
export CATALINA_HOME=/opt/tomcat

exec jhsingle-native-proxy --debug --logs --authtype none --request-timeout 15 --destport 8080 -- /opt/tomcat/bin/catalina.sh run
