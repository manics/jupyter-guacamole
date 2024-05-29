# Ubuntu Mate desktop with Firefox, Conda and JupyterLab
FROM docker.io/library/ubuntu:24.04

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
    apt-get install -y -q --allow-downgrades firefox && \
    apt-get purge -y -q \
        blueman \
        mate-screensaver \
        update-notifier && \
    apt-get autoremove -y -q

RUN mkdir -p /opt/conda/Desktop /opt/conda/icons && \
    chown -R ubuntu:ubuntu /opt/conda

USER ubuntu
WORKDIR /home/ubuntu

ARG MAMBAFORGE_VERSION=24.3.0-0
RUN curl -sfL https://github.com/conda-forge/miniforge/releases/download/$MAMBAFORGE_VERSION/Mambaforge-$MAMBAFORGE_VERSION-Linux-`uname -m`.sh -o Mambaforge.sh && \
    bash Mambaforge.sh -b -f -p /opt/conda && \
    rm -f Mambaforge.sh
COPY --chown=ubuntu:ubuntu environment.yml /opt/conda/environment.yml
RUN /opt/conda/bin/mamba init && \
    /opt/conda/bin/mamba env update --file /opt/conda/environment.yml

COPY --chown=ubuntu:ubuntu jupyter_logo.svg /opt/conda/icons/jupyter_logo.svg
COPY --chown=ubuntu:ubuntu jupyterlab.desktop /opt/conda/Desktop/jupyterlab.desktop

RUN mkdir /home/ubuntu/Desktop && \
    ln -s \
        /usr/share/applications/mate-terminal.desktop \
        /usr/share/applications/firefox.desktop \
        /opt/conda/Desktop/jupyterlab.desktop \
        /home/ubuntu/Desktop

USER root
# /home/ubuntu may be overwritten with a persistent volume
# Create a copy and restore on first start if necessary
RUN rsync -a /home/ubuntu/ /home/ubuntu.orig/

COPY start-mate.sh /usr/local/bin/start-mate.sh
COPY start.sh /usr/local/bin/start.sh

USER ubuntu
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

EXPOSE 5901
CMD ["/usr/local/bin/start.sh"]
