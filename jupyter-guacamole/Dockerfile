################################################################################
FROM docker.io/library/ubuntu:22.04

USER root

RUN apt-get -y -q update && \
    apt-get install -y -q \
    curl \
    default-jre-headless \
    python3-pip \
    tar

RUN cd /opt && \
    curl -sfL https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-home/10.0.14/jetty-home-10.0.14.tar.gz | tar -zx
ENV JETTY_HOME=/opt/jetty-home-10.0.14

RUN python3 -mpip install jhsingle-native-proxy==0.8.0

# Use 1000:1000 to match the default Jupyter user
ARG UID=1000
ARG GID=1000
RUN groupadd --gid $GID guacamole
RUN useradd --system --create-home --shell /usr/sbin/nologin --uid $UID --gid $GID guacamole
WORKDIR /home/guacamole

ARG GUACAMOLE_JUPYTER_VERSION=1.5.0
ARG GUACAMOLE_JUPYTER_TAG=1.5.0-jupyter.0
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
