# Configuration file for JupyterHub
import os
import sys

c = get_config()  # noqa: F821


c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name


c.DockerSpawner.volumes = {"jupyterhub-user-{username}": "/home/ubuntu"}

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.Spawner.debug = True

c.Spawner.environment = {
    # VNCserver should listen on public port
    "LOCALHOST": "no",
    "STATIC_REDIRECTOR_DESTINATION": os.environ["JUPYTERHUB_GUACAMOLE_SERVICE"],
}

# Need to sleep to give time for the process to be backgrounded
c.DockerSpawner.post_start_cmd = "bash -c 'nohup /usr/local/bin/start.sh & sleep 1'"

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

c.JupyterHub.authenticator_class = "dummy"

c.JupyterHub.services = [
    {
        "name": "guacamole",
        "url": "http://127.0.0.1:10102",
        "command": [sys.executable, "./guacamole_handler/guacamole_handler.py"],
        "environment": dict((k, os.environ[k]) for k in [
            "JSON_SECRET_KEY",
            "GUACAMOLE_HOST",
            "GUACAMOLE_PUBLIC_HOST",
        ]),
        "oauth_client_allowed_scopes": ["read:users!user"],
    },
]

c.JupyterHub.load_roles = [
    {
        "name": "admin",
        "users": ["admin"],
    },
    {
        "name": "user",
        # grant all users access to all services
        "scopes": ["access:services", "self"],
    },
]

# Don't automatically go to server, easier to test hub
c.JupyterHub.default_url = "/hub/home"

c.Application.log_level = "DEBUG"
