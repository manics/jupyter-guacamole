################################################################################
# https://www.docker.com/blog/faster-multi-platform-builds-dockerfile-cross-compilation-guide/
# FROM --platform=$BUILDPLATFORM docker.io/library/maven:3.8.4-openjdk-8 as client-builder
FROM docker.io/library/maven:3.8.4-openjdk-8 as client-builder

RUN git clone --depth=1 --branch=1.4.0-jupyterhub https://github.com/manics/guacamole-client.git /guacamole-client
# RUN git clone --depth=1 --branch=jupyterhubnotatre https://github.com/manics/guacamole-client.git /guacamole-client

RUN cd /guacamole-client/guacamole && \
    mvn package -Dmaven.test.skip=true -Dmaven.javadoc.skip=true
RUN cd /guacamole-client/extensions/jupyternotatre-auth && \
    mvn package -Dmaven.test.skip=true -Dmaven.javadoc.skip=true


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

RUN useradd --system --create-home --shell /usr/sbin/nologin guacamole
WORKDIR /home/guacamole

COPY --chown=guacamole:guacamole --from=client-builder /guacamole-client/guacamole/target/guacamole-1.4.0.war /home/guacamole/webapps/ROOT.war
COPY --from=client-builder /guacamole-client/extensions/jupyternotatre-auth/target/jupyternotatre-auth-1.4.0.jar /etc/guacamole/extensions/

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
