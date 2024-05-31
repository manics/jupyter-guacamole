# Jupyter Guacamole

[![Build](https://github.com/manics/jupyter-guacamole/actions/workflows/build.yml/badge.svg)](https://github.com/manics/jupyter-guacamole/actions/workflows/build.yml)

**⚠️⚠️⚠️⚠️⚠️ Under development ⚠️⚠️⚠️⚠️⚠️**

An example of running a Linux desktop in a Jupyter environment using Guacamole.

This contains container images for

- A Ubuntu MATE desktop with VNC and no auth
- A Guacamole client with [jhsingle-native-proxy](https://github.com/ideonate/jhsingle-native-proxy)

Build Ubuntu desktop and Guacamole images

```
docker-compose build
```

Start all containers (Ubuntu desktop, Guacamole server (upstream guacd image), Guacamole client)

```
docker-compose up
```

Open http://localhost:8888/

The Guacamole control panel can be opened with `<Ctrl>+<Alt>+<Shift>`
https://guacamole.apache.org/doc/gug/using-guacamole.html
