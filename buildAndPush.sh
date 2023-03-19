#!/bin/bash

docker build . -t docker.io/jozseftorocsik/szakdolgozat-monitor --no-cache
docker push docker.io/jozseftorocsik/szakdolgozat-monitor


helm uninstall monitor -n apps
helm install monitor ./helm/monitor -n apps
