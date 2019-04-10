

# Virtuin Starter

This repo contains a simple starter to begin creating tasks and applications in
Virtuin. The tasks are currently written in python, however you can use whatever
tools and platforms you prefer.

### To Begin

* clone this repo
* set VIRT_STATION_NAME on your computer globally to VIRT_DEFAULT_STATION
  - open collection.yml at the root
  - change the value of **stationCollectionEnvPaths -> VIRT_DEFAULT_STATION** with the absolute path of this repo.
  - you can change station name later and modify stationCollectionEnvPaths appropriately
* load the root collection.yml from the Virtuin GUI


### Contents

- collection.env : currently empty, however environment variables can be added
as needed.
- collection.yml : development collection with two groups of tasks. First group
has one task, which can be run as needed by the operator. Second group is managed
so the REST API is used to enable and reset the status of tasks. The *dockerCompose*
consists of an nginx web service so that files can be retrieved from the docker environment.
It also consists of two services to build from source. Each of which contain the executables to
run as *Tasks*. The path's use
**VIRT_COLLECTION_ENV_PATH**, which will be set the corresponding path of
matching station name in **stationCollectionEnvPaths**.


see [Virtuin](https://github.com/cpsamtec/virtuin) documentation for more help

When you have finished developing you will want to convert into a release build.
When released all of docker build source will be converted to images placed on docker
hub. Instead of specifying builds in the docker compose, you will specify the
image.
 A development build
will display extra features in the GUI. To create a release build

1. change build key value in collection.yml to *release*
2. build all of your docker src directories and create images
3. push the docker images to docker hub
4. modify your docker compose source section of collection.yml to use the
images as opposed to the build directories.  
5. add any known stations with a corresponding collection.env to **stationCollectionEnvPaths**.

```
collectionName: Virtuin_Starter
build: release
stationCollectionEnvPaths:
  VIRT_DEFAULT_STATION: "/station's/full/path/to/collection.env"
  SOME_OTHER_STATION: "/this/station/path/to/collection.env"
taskGroups:
......
dockerCompose:
  source:
  ......

```
6. make the new collection.yml available on a web server or copy to desired
stations.

If you are using private images make sure to have appropriate docker login credentials set in the collection.env of each station the application will be running.

The root collection is a *development* build. To see a release version of the
collection.yml view the release folder.
