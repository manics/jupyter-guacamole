FROM docker.io/library/ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y -q
RUN apt-get install -y -q \
  mate-desktop-environment-core \
  tigervnc-standalone-server

RUN apt-get install -y -q ubuntu-mate-desktop

COPY start-mate.sh /usr/local/bin/start-mate.sh

RUN useradd -m ubuntu

USER ubuntu
WORKDIR /home/ubuntu

# TODO: when this is in a pod set `-localhost yes` since all containers in a pod share the same network namespace
CMD ["/usr/bin/tigervncserver", ":1", "-fg", "-localhost", "no", "--I-KNOW-THIS-IS-INSECURE", "-SecurityTypes", "None", "-xstartup", "/usr/local/bin/start-mate.sh"]
EXPOSE 5901
