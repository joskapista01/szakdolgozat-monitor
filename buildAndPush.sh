#!/bin/bash

docker build . -t docker.io/jozseftorocsik/szakdolgozat-monitor --no-cache
docker push docker.io/jozseftorocsik/szakdolgozat-monitor


#helm uninstall api -n apps
#helm install api ./helm/api -n apps
