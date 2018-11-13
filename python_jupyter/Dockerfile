
FROM debian:stable
MAINTAINER gguida <gl-ai-datascience-core@coolblue.nl>

ENV HOME /opt
ENV MODULENAME recommendersystems
ENV variable=exp

## Install linux packages
RUN echo 'deb-src http://deb.debian.org/debian stretch main' >> /etc/apt/sources.list \
    && apt-get update  -y \
    && apt-get upgrade -y\
    && apt-get install -y \
        build-essential \
        curl \
        openssh-server \
        make \
        net-tools\
        pkg-config \
        pigz \
        wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $HOME
RUN wget https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh \
    && /bin/bash Miniconda3-4.2.12-Linux-x86_64.sh -b
ENV PYTHON_BIN_PATH=$HOME/miniconda3/bin
ENV PYTHON_EXECUTABLE=$PYTHON_BIN_PATH/python
ENV PIP_EXECUTABLE=$PYTHON_BIN_PATH/pip

# create links
RUN ln -s $PYTHON_EXECUTABLE /usr/bin/python
RUN ln -s $PIP_EXECUTABLE /usr/bin/pip

# Install python packages
# Important note: pycharm outmatically mounts the project folder in $HOME this way: $HOME/project/recommendersystems
ENV WORKING_DIR_PATH $HOME/project/$MODULENAME
WORKDIR $WORKING_DIR_PATH
RUN echo $WORKING_DIR_PATH
RUN echo $WORKING_DIR_PATH/requirements.txt

COPY requirements.txt $WORKING_DIR_PATH/requirements.txt
COPY requirements-dev.txt $WORKING_DIR_PATH/requirements-dev.txt
RUN $PIP_EXECUTABLE install --upgrade pip \
    && $PIP_EXECUTABLE install -r $WORKING_DIR_PATH/requirements.txt \
    && $PIP_EXECUTABLE install -r $WORKING_DIR_PATH/requirements-dev.txt
RUN rm -r $HOME/.cache/pip
