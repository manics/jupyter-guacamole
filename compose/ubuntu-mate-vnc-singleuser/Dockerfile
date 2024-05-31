FROM ghcr.io/manics/ubuntu-mate-vnc:main

RUN /opt/conda/bin/mamba create -y -n singleuser python=3.11 pip

RUN /opt/conda/envs/singleuser/bin/pip install \
        jupyter-server \
        jupyterhub

ADD static_redirector /src/static_redirector
RUN /opt/conda/envs/singleuser/bin/pip install /src/static_redirector

CMD /opt/conda/envs/singleuser/bin/jupyterhub-singleuser
