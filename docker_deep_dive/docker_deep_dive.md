# Docker deep dive

## Recap
docker stop `docker ps -a -q`
docker run -itd ubuntu:xenial /bin/bash  It runs deamonized ("/bin/bash" is the default command)
docker restart container name # you can skip this
docker attach container name # will login the docker
apt-get update
exit # will cause the docker to stop
docker inspect | grep Status # will result in the container not running
docker inspect | grep IP # will result in no ip configured

Important: data is not lost when a docker container stops (Try creating a file and restarting it)

You can commit changes to a container, creating a new image, (for instance a file is created or software installed)
`docker commit -m "Changes happened here" -a "giuseppe-guida" container_name` giuseppe/ubuntu:v1
it restults in a new image. In this way we haven't created a docker file yet.

## Running Container Commands with Docker

How can we interact with docker containers?

If i want to see the latest commands run in the container,
docker logs container_name

Three ways to run a process in a container:
```commandline
docker exec container_name /bin/cat /etc/profile # on a running container

or

docker run ubuntu:xenial /bin/echo "Hello world" # this starts a new container
docker restart new_container_name # will print "Hello World" again! (because the command for the container becomes echo hello world)

or

docker run -d ubuntu:xenial /bin/bash -c "while true; echo HELLO; sleep 1;done" # this will run forever in as a deamon
docker logs container_name | wc -l # run multiple times will print an increasing number, until the container is stopped
```

## Port redirection

For the container to listen on a port, that port needs to be exposed to the underlying host. We can expose ports using the Dockerfile.

docker run -d nginx:latest (starts with the default command)
docker inspect container_name | grep IP
elinks http://172.17.0.2 # will open the elinks text browser and show the Welcome to nginx page

Any service available in the container is available only on the IP of the container.

elinks http://localhost # will fail
That's because i have nothing running on the localhost itself and localhost can't redirect me to any service in the container.

docker run -d -p 8080:80 nginx:latest # will redirect my localport 80 to the container's port 80
docker ps shows the following
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                NAMES
0fde190eaf35        nginx:latest        "nginx -g 'daemon of…"   13 seconds ago      Up 12 seconds       0.0.0.0:8080->80/tcp   determined_panini

0.0.0.0:8080->80/tcp
stands for redirect the localhost (0.0.0.0) port (8080) to the container's port (80) # THIS IS A PORT PASS THROUGH

now elinks http://172.17.0.2:80 and elinks http://localhost:8080 both work!

This is useful because multiple engines containers can be running at the same time (for instance multiple services or multiple environments)

## Dockerfile Directives: USER and RUN

