################################################################################
FROM docker.io/library/ubuntu:24.04

USER root

RUN apt-get -y -q update && \
    apt-get install -y -q \
    curl \
    default-jre-headless \
    python3-pip \
    python3-venv \
    tar

ARG JETTY_VERSION=10.0.24
RUN cd /opt && \
    curl -sfL https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-home/$JETTY_VERSION/jetty-home-$JETTY_VERSION.tar.gz | tar -zx
ENV JETTY_HOME=/opt/jetty-home-$JETTY_VERSION

RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/python -mpip install jhsingle-native-proxy==0.8.3

# Use 1000:1000 to match the default Jupyter user
ARG USERID=1000
ARG GROUPID=1000
RUN userdel -r ubuntu && \
    groupadd --gid $GROUPID guacamole && \
    useradd --system --create-home --shell /usr/sbin/nologin --uid $USERID --gid $GROUPID guacamole
WORKDIR /home/guacamole

ARG GUACAMOLE_JUPYTER_VERSION=1.5.5
ARG GUACAMOLE_JUPYTER_TAG=1.5.5-jupyter.0
RUN mkdir -p \
        /home/guacamole/webapps \
        /etc/guacamole/extensions && \
    curl -sfL https://github.com/manics/guacamole-client/releases/download/${GUACAMOLE_JUPYTER_TAG}/guacamole-${GUACAMOLE_JUPYTER_VERSION}.war \
        -o /home/guacamole/webapps/ROOT.war && \
    chown -R guacamole:guacamole /home/guacamole/webapps/ && \
    curl -sfL https://github.com/manics/guacamole-client/releases/download/${GUACAMOLE_JUPYTER_TAG}/jupyternotatre-auth-${GUACAMOLE_JUPYTER_VERSION}.jar \
        -o /etc/guacamole/extensions/jupyternotatre-auth-${GUACAMOLE_JUPYTER_VERSION}.jar

# /etc/guacamole/guacamole.properties will be updated at runtime
RUN touch /etc/guacamole/guacamole.properties && \
    chown guacamole /etc/guacamole/guacamole.properties

USER guacamole
# Jetty modules:
# https://www.eclipse.org/jetty/documentation/jetty-10/operations_guide.php
RUN java -jar $JETTY_HOME/start.jar --add-modules=deploy,debug,http,requestlog,websocket

# COPY logging.properties /opt/tomcat/conf/logging.properties
COPY logback.xml /etc/guacamole/
COPY start.sh /usr/local/bin/start.sh

EXPOSE 8080
CMD ["/usr/local/bin/start.sh"]
