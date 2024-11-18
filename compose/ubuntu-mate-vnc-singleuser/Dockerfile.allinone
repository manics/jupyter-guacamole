FROM ghcr.io/manics/ubuntu-mate-vnc:main

# jupyterhub-singleuser conda requires jupyterlab
# jupyterhub-base provides jupyterhub-singleuser
RUN /opt/conda/bin/mamba create -y -n singleuser \
    python \
    pip \
    jupyter_server \
    jupyterhub-base

COPY static_redirector /src/static_redirector
RUN /opt/conda/envs/singleuser/bin/pip install /src/static_redirector

COPY jupyter_server_config.py /opt/conda/etc/jupyter/

CMD ["/opt/conda/envs/singleuser/bin/jupyterhub-singleuser"]
