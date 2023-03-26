# Ubuntu Mate desktop with Firefox, Conda and JupyterLab
FROM docker.io/library/ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

# Ubuntu 22.04 installs firefox from snap by default
# https://www.omgubuntu.co.uk/2022/04/how-to-install-firefox-deb-apt-ubuntu-22-04
# Note Firefox sandboxing may not work, to disable it see
# https://wiki.mozilla.org/Security/Sandbox#Environment_variables
RUN apt-get update -y -q && \
    apt-get install -y -q \
        curl \
        dumb-init \
        jq \
        less \
        tigervnc-standalone-server \
        ubuntu-mate-desktop \
        vim && \
    add-apt-repository -y ppa:mozillateam/ppa && \
    printf 'Package: firefox*\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 1001\n' > /etc/apt/preferences.d/firefox && \
    apt-get install -y -q firefox && \
    apt-get purge -y -q mate-screensaver && \
    apt-get autoremove -y -q

RUN useradd -m ubuntu -s /usr/bin/bash

USER ubuntu
WORKDIR /home/ubuntu

ARG MAMBAFORGE_VERSION=22.11.1-4
RUN curl -sfL https://github.com/conda-forge/miniforge/releases/download/$MAMBAFORGE_VERSION/Mambaforge-$MAMBAFORGE_VERSION-Linux-`uname -m`.sh -o Mambaforge.sh && \
    bash Mambaforge.sh -b -f -p ~/conda && \
    rm -f Mambaforge.sh
COPY --chown=ubuntu:ubuntu environment.yml /home/ubuntu/environment.yml
RUN ~/conda/bin/mamba init && \
    ~/conda/bin/mamba env update --file /home/ubuntu/environment.yml

RUN mkdir /home/ubuntu/Desktop && \
    ln -s /usr/share/applications/mate-terminal.desktop /home/ubuntu/Desktop/mate-terminal.desktop && \
    ln -s /usr/share/applications/firefox.desktop /home/ubuntu/Desktop/firefox.desktop

COPY --chown=ubuntu:ubuntu jupyter_logo.svg /home/ubuntu/.icons/jupyter_logo.svg
COPY --chown=ubuntu:ubuntu jupyterlab.desktop /home/ubuntu/Desktop/jupyterlab.desktop

COPY start-mate.sh /usr/local/bin/start-mate.sh
COPY start.sh /usr/local/bin/start.sh

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

EXPOSE 5901
CMD ["/usr/local/bin/start.sh"]
