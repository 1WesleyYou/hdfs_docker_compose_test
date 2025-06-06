#!/bin/bash

echo "apply the given yamls"
kubectl apply -f 00-hdfs-configmap.yaml   \
              -f 01-hdfs-headless-svc.yaml \
              -f 02-namenode-statefulset.yaml \
              -f 03-datanode-statefulset.yaml \
              -n hdfs-chaos

