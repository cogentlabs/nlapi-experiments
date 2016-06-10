


##Dockerized server

Build the server image:

```
docker build -t attachment-finder-server .
```

Run with port 5000 mapped, connect at <container_addr>:5000

```
docker run -d -p 5000:5000 attachment-finder-server
```

If using docker-machine, probably just use that network bridge and connect at <docker_machine_addr>:5000

```
docker run -d --net=host attachment-finder-server 
```
