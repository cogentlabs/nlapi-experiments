FROM node:latest

MAINTAINER Joe Bullard <jbullard@reactive.co.jp>

RUN apt-get update \
    && apt-get -y install python-numpy python-flask \
    && apt-get clean \
    && rm -rf /var/cache/apt/lists/*

WORKDIR /attachment-finder

ADD . .

# This could be done better, but I'm really not familiar with node
RUN npm install lodash path fs-promise axios yargs

EXPOSE 5000

CMD [ "/bin/bash", "-c", "/usr/bin/python2 server.py" ]
