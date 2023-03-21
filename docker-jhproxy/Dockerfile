FROM docker.io/library/python:3.11-bullseye

RUN apt-get update -y -q && \
    apt-get install -y -q socat

RUN pip install jhsingle-native-proxy

COPY start.sh /usr/local/bin/start.sh
ENTRYPOINT ["/usr/local/bin/start.sh"]
