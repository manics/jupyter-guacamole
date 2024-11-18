# JupyterHub Guacamole Service Docker Compose Example

**⚠️⚠️⚠️⚠️⚠️ WARNING: This is a proof of concept, it is not secure! ⚠️⚠️⚠️⚠️⚠️**

Build images, then run JupyterHub on http://localhost:8000 and Guacamole on http://localhost:8080/guacamole

```
podman-compose build
podman-compose up
```

1. Login to http://localhost:8000 with any username/password (dummy authenticator)
2. Start a server
3. You should be directed to a JupyterHub Guacamole token service
4. Accept the OAuth prompt (this can be turned off)
5. You should be redirected to a Guacamole desktop


## How this works

The singleuser server contains a minimal Jupyter server application (needed to communicate with JupyterHub), and a Ubuntu MATE Desktop.
In Kubernetes this could be split into two containers in the same pod for additional security.

Guacamole is configured with [Encrypted JSON authentication](https://guacamole.apache.org/doc/gug/json-auth.html).
Any client with the secret key can create a Guacamole connection.

There is a [JupyterHub service for creating Guacamole tokens](hub/guacamole_handler.py), which uses the secret key to create a Guacamole VNC connection to `jupyter-<username>:5901`.
This service uses JupyterHub OAuth, so when the user visits the service the user's identity is known.



