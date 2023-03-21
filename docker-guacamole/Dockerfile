################################################################################
FROM docker.io/library/maven:3.8.4-openjdk-8 as client-builder

RUN git clone --depth=1 --branch=1.4.0-jupyterhub https://github.com/manics/guacamole-client.git /guacamole-client
RUN cd /guacamole-client && \
    mvn package -Dmaven.test.skip=true -Dmaven.javadoc.skip=true
    #-DignoreLicenseErrors=true


################################################################################
# https://github.com/apache/guacamole-server/blob/1.4.0/Dockerfile
FROM docker.io/guacamole/guacd:1.4.0

USER root

RUN apt-get -y -q update && \
    apt-get install -y -q \
    curl \
    default-jre-headless \
    python-pip \
    supervisor

# Guacamole is incompatible with Tomcat 10
# https://issues.apache.org/jira/browse/GUACAMOLE-1325
ARG TOMCAT_VERSION=9.0.73
ARG TOMCAT_SHA512=d43fbd6c5ae00bc0ffc2559743f91abd3547c827426cb0acdc8428e060e8659b6bb41b3877deb061ab6202980de39b9558525a4256725b647d5bff93e47a5664
RUN curl -sfLO https://dlcdn.apache.org/tomcat/tomcat-${TOMCAT_VERSION%%.*}/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz && \
    echo "${TOMCAT_SHA512} apache-tomcat-${TOMCAT_VERSION}.tar.gz" | sha512sum -c - && \
    mkdir -p /opt/tomcat && \
    tar -xf apache-tomcat-${TOMCAT_VERSION}.tar.gz -C /opt/tomcat --strip-components=1 && \
    rm apache-tomcat-${TOMCAT_VERSION}.tar.gz && \
    rm -rf /opt/tomcat/webapps/* && \
    chmod -R a+rX /opt/tomcat && \
    chmod -R a+x /opt/tomcat/bin/*.sh

COPY --from=client-builder /guacamole-client/guacamole/target/guacamole-1.4.0.war /opt/tomcat/webapps/ROOT.war
COPY --from=client-builder /guacamole-client/extensions/jupyternotatre-auth/target/jupyternotatre-auth-1.4.0.jar /etc/guacamole/extensions/

ENV PATH /opt/tomcat/bin:$PATH

RUN pip install supervisor-stdout==0.1.1

# Create a new user guacamole
ARG CLIENT_UID=1001
ARG CLIENT_GID=1001
RUN groupadd --gid $CLIENT_GID guacamole
RUN useradd --system --create-home --shell /usr/sbin/nologin --uid $CLIENT_UID --gid $CLIENT_GID guacamole

RUN cd /opt/tomcat && \
    chown guacamole conf logs temp webapps work
ADD logging.properties /opt/tomcat/conf/logging.properties
ADD guacamole.properties /etc/guacamole/guacamole.properties
ADD logback.xml /etc/guacamole/

ADD supervisord.conf /etc/supervisor/

EXPOSE 8080
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]

# http://localhost:18080/guacamole
