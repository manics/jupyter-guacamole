# Jupyter Guacamole

**⚠️⚠️⚠️⚠️⚠️ Under development ⚠️⚠️⚠️⚠️⚠️**


Build Ubuntu desktop and Guacamole images
```
podman build -t docker-ubuntu-mate ./docker-ubuntu-mate
podman build -t docker-guacamole ./docker-guacamole
```

Run the Ubuntu MATE desktop in one terminal:
```
podman run -it --rm --name ubuntu -p 5901:5901 docker-ubuntu-mate
```
Run Guacamole in another terminal, setting `HOSTNAME` to the IP address of the host machine (needed to connect to VNC in the Ubuntu container):
```
podman run -it --rm --name guac -p 8080:8080 -ePROTOCOL=vnc -eHOSTNAME=192.168.1.1 docker-guacamole
```

At this point you should be able to connect to the Ubuntu desktop in your browser at http://localhost:8080

To run this in JupyterHub a singleuser server proxy is needed, in this case [jhsingle-native-proxy](https://github.com/ideonate/jhsingle-native-proxy):

```
podman build -t docker-jhproxy ./docker-jhproxy
```

Run, replacing `192.168.1.1` with the IP address of the host machine, and setting a pretend user prefix:
```
podman run -it --rm --name jhproxy -e JUPYTERHUB_SERVICE_PREFIX=/user/abc -p8888:8888 docker-jhproxy 192.168.1.1:8080
```
Open http://localhost:8888/user/abc

The Guacamole control panel can be opened with `<Ctrl>+<Alt>+<Shift>`
https://guacamole.apache.org/doc/gug/using-guacamole.html
