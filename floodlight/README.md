# Floodlight Setup Instructions

## Prerequisites
- Docker (engine & compose)
- Fast internet connection (might want to do this on the university network)
- A clone of this repository

## Installing Docker
Docker can be obtained through following the instructions at:
https://docs.docker.com/engine/getstarted/step_one/

## Runnning the Container
- Navigate to the `floodlight` folder within the clone of this repository:

`$ cd <repo_path>/floodlight`
- Run from the docker-compose file:

`$ docker build -t floodlight .`
- NOTE: The first time this is run it will build the image before running. This will take a pretty long time. The image has to obtain the apt-cache, install a bunch of development packages, download the source for floodlight (which is BIG), and then do a build.
- NOTE2: When building it will look as if the `cloning into floodlight...` step has frozen. It hadn't it just doesn't output from within the docker build script. It will take a while, but it will complete.

- You can then access the web-ui for floodlight by navigating to:

`http://127.0.0.1:8080/ui/pages/index.html`
- The container can be stopped by issuing:

`docker-compose stop`


