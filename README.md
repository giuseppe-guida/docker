# Docker Quick Start

## Installation and configuration

### Installation on Centos 7
```
using root

cd /et/yum.repos.d
vim docker.repo # creates a repository

	[dockerrepo]
	name=DockerRepository
	baseurl=htt://yum.dockerproject.org/repo/main/centos/7/
	enable=1
	gpgcheck=1
	pgkey=https://yumdockerproject.org/gpg

yum update # will download the docker application

yum install -y docker-engine # install docker-engine
```

###### set up services
```
systemctl enable docker # creates the link for starting the service
systemctl start docker # now the docker deamon (service) runs, we con connect to it, also from remote
docker --version
docker images
```

###### security
It's not a good idea to user the root though
```
logout
docker images #can't connect

sudo su
cd /var/run
ls -al dock*
docker.pid
docker.sock # we have to be able to connect to this using the user group docker, therefore we need to add the user to the docker group

cat /etc/group | grep docker

usermod -a -G docker user #adds the user user to the docker group
```

### Installation on MacOSX
simply run the command `brew install docker`

## Getting a base image
```
docker search an_image
docker pull imageid
docker inspect imgeid
docker start imageid
docker ps -a # all includes also the recently running containers
docker stop containerid
docker rmi [imageid|containerid] # this removes the downoloaded repository. remember to remove the container first
```

## Lifecycle

Once it's up we can look at the list of running containers `docker ps # -a includes previously running too`

Important difference:
`docker run` is used to run an image = create a container and execute the container
`docker start` is used on a container previously run


We can also run containers as deamons

```
docker run -d --name=MyWeb1 centos:latest # -d deactive (aka deamon) and we can do it multiple times spcifing different aliases which will cause them to have diffrent ip addresses```

or interactively

docker run -it centos:latest /bin/bash # run interactively -i the centos docker in the terminal -t running the command /bin/bash (it runs the bash). It logs in as root user```
```
or we can run a process in this whalesay
```
docker run docker/whalesay cowsay hello # runs the application cowsay and exit' this can kill the DockerRepository`
```

The best way to launch a process in an existing docker container wihtout causing it to be killed on the exit is this:

```
docker exec -it centos:latest /bin/bash/ # doesn't affect the execution of the current started process
```

in this case it is interactive but it shouldn't be.

To remove all the stopped containers: ``docker rm `docker ps -a -q` ``  only the no currently running or `docker rm $(docker ps -a -q)`
## Ports and Volumes

Why ports and rediraction is important?
I dont have to worry about routing and I can say that on each port theres a different sever listening eg. dev/acc/prod

```
docker run nginx:latest
docker ps # shows two ports available like 80/tcp and 443/tcp
docker inspect containerid | grep IPAddr
```

if i run eliniks on `http://x.x.x.x` it works
if i run eliniks on `http://localhost:8080` it doesn't work

why? I need to enable the routing from the host computer to that specific port exposed b the container

how to redirect those availalbe ports to localhost?
`docker run -d -P --name=WebServer1 nginx:latest`
**-P**: any port exposed to my container makes it available through the host operating system on a random port
or `docker run -d -p 8080:80 --name=WebServer1 nginx:latest` which will map the host port 8080 to the container port 80.
`docker ps` shows as ports available 0.0.0.0:32771->80/tcp standing for **the port 32771 is bound to all local interfaces, local host as well to the ip bound to this localhost**
you can also see that from `docker port containerid $CONTAINERPORT`

there are two ways to connect to that container:
1. through its IP if i have routing to and from among the host that it exists on
2. or if im on the network of my host or anybody who can see that that IP address is along the port with it then i can connect to it

Another advantage: in this way you can mount directories through the host on the container
`docker run -d -p 8080:80 --name=WebServer3 -v /mnt/data nginx latest`

```
cd $HOME
mkdir wwww
cd www
vim index.html [write a simple html page]
docker run -d -p 8080:80 --name=WebServer4 -v /home/user/www:/usr/share/nginx/html nginx:latest
elinks http:localhost:8080 # shows the index.html from the localhost
[change the html here]
elinks http:localhost:8080 # shows a different html file
```

*/home/user/www:/usr/share/nginx/html* is the default location for the nginx server


I can for instance make a backup of a database writing straight away to the host directory.

## The docker file

Example of docker file:

```
FROM debian:stable
MAINTAINER gguida <email@gmail.com>

# runs using the root account
RUN apt-get update
RUN apt-get upgrade
RUN apt-get install telnet
RUN echo "This command is executed when the image is created"
CMD echo "This command is executed only when the image is instantiated, aka the container is created"
```

Note:
- RUN is exectud when creating the image (&& stops as soon as the previous command doesn't succeed)
- CMD executed when on the instantiated container of the base image


now build from the same directory of the file
`docker build -t latest123/myapache /docker_file_dir`
Note: mulitple runs used cached copies

This script is not a best practice because there are multiple layers that are created for each command executed. We can run ecerythin in one single layer.

Best practice:
```
# Docker docker docker_file_dir
FROM debian:stable
MAINTAINER gguida <email@gmail.com>

# runs using the root account
RUN apt-get update && apt-get upgrade -y && apt-get install -y apache2 telnet elinks open-ssh

ENV MYVALUE myvalue

EXPOSE 80 # expose this port through the host using mapping redirect in the section Ports and Volumes

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"] # ["command", "option1", "option2"]. In this case -D stands for running the command as a Deamon
```
_Note: this image, when instanciated will run automatically the Apache server in Daemon mode so that we can connect to it and check out the server name_

To check that everything ran correctly:
```
docker inspect containerid | grep IPAdr # get the ip addres
elinks http://172.17.0.2 # will open the docker container
docker exec -it container-id /bin/bash
ps aux | grep apache # will show that the process is running as a daemon
echo $MYVALUE
exit
```

## Clean up
`docker system prune` remove all images that are not associated with a container

`docker rm containerid` remove a container id

`docker rmi imageid` remove an imageid

## Other useful commands

### mount volume from interactive shell
docker run -it -v /Users/giuseppeguida/Downloads:/data:rw centos:latest /bin/bash

### ...
