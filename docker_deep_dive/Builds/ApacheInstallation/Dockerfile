FROM centos:latest
MAINTAINER peppe.guida@gmail.com

RUN yum update -y
RUN yum install -y httpd net-tools

RUN echo "This is a custom index file build during image creation" > /var/www/html/index.html

EXPOSE 80

ENTRYPOINT apachectl "-DFOREGROUND" # command that runs if no other commands are passed in the `docker run -it command`.

