#!/bin/bash

echo "将本进程的 config 文件设置为当前路径下的 kubeconfig.yaml 文件"
export KUBECONFIG=$(pwd)/kubeconfig.yaml
kubectl get nodes
