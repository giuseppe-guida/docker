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

When a docker is created the command is run as root user autmatically (example docker run -itd /bin/bash)
Ideal, create a non proviliged user.

Build the folllowing image `docker build -t cenots7/nonroot:v1`

```Dockerfile
# Dockerfile based on the latest CentOS 7 image - non provileged user entry
FROM centos:latest
MANTAINER peppe.guida@gmail.com

RUN useradd -ms /bin/bash username **
RUN echo "this command won't fail" >> /etc/exports.list   # runs as root user

RUN wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2Ftechnetwork%2Fjava%2Fjavase%2Fdownloads%2Fjdk8-downloads-2133151.html; oraclelicense=accept-securebackup-cookie;" "http://download.oracle.com/otn-pub/java/jdk/8u171-b11/512cd62ec5174c3487ac17c61aaa89e8/jdk-8u171-linux-x64.rpm"

RUN yum localinstall -y ~/jdk-8u171-linux-x64.rpm # So it also picks the proper dependencies

USER username  # switches to another user. From this moment the user switches and also the concept of home directory.

RUN echo "this command will fail" >> /etc/exports.list   # if run here it will fail becase we havven't granted any right to do so to the username. THE ORDER OF EXECUTION MATTERS

RUN cd ~ && "export JAVA_HOME=/usr/java/jdk1.8.0/jre" >> /home/user/.bashrc # This adds the env variable only for the username user. Therefore not for the root user or other users. The ENV directive helps in that case.

ENV JAVA_BIN /usr/java/jdk1.8.0/jre/bin # This is equivalent to the previous command but for all users

CMD echo "This command is executed at run time"

ENTRYPOINT "This command will run for EVERY container that is run from it" # It always run and can't be modified by the run command, differently from the CMD that could be modified. Check this better
```

** Creates a user including the home directory (-m) and the user's login shell (-s, in this case /bin/bash). Running this cantainer wihtout this won't work! `docker run -it centos7/nonroot:v1 /bin bash` will result in the error `linux spec user unable to find the user` because the user won't be found!

It's important to know that by running the docker with a specific user we can't switch to the sudo - su (the passwrod will be asked but it won't exist). This is a desired beheaviour, indeed that shouldnt' be possible when a container is deployed and distributed (the container, not the image).

Connecting as super user is still possible through `docker run -u 0 -it /bin/bash`. When that happens, by running `ps aux` you'll see two /bin/bash processes running, one as root and another as username. By exiting, the docker container will still be running as username but not as root. That's also desired.
