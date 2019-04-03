

# Virtuin Starter

This repo contains a simple outline to begin creating tasks and applications in
Virtuin. It is composed primarily of a

- collection.yml : contains details of the tasks and embedded docker-compose
- collection.env : add environment variables
- src : directory contain all of the subdirectories to build the various docker
compose services. Basic python examples have been added.


To begin using
* make sure to have VIRT_STATION_NAME set on your computer
* clone this repo
* load the collection.yml from the Virtuin GUI

see Virtuin documentation for more help

When you have finished developing you will want to convert into a release mode.
When released all of your docker will be converted to images placed on a docker
hub. Instead of specifying builds in the docker compose you will specify the
image.
The collection is currently in development mode. To create a release mode

1. change mode in collection.yml to *release*
2. build all of your docker src directories and create images
3. push the docker images to docker hub
4. modify your docker compose source section of collection.yml to use the
images as opposed to the build directories.  
