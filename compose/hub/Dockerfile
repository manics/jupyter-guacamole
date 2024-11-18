# A standalone JupyterHub guacamole_handler service
# Use this for Z2JH where a hub-managed service URL doesn't work
# because localhost can't be accessed by configurable HTTP proxy
# running separately, and we don't know the network iface to use
#
# docker.io/manics/jupyterhub-guacamolehandler
ARG JUPYTERHUB_VERSION=5.2.1
FROM quay.io/jupyterhub/jupyterhub:$JUPYTERHUB_VERSION

COPY guacamole_handler /opt/guacamole_handler

CMD ["python", "/opt/guacamole_handler/guacamole_handler.py"]
