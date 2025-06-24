#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
set +u

export HADOOP_HOME=/users/yuchenxr/hadoop/hadoop-dist/target/hadoop-3.1.2

if [ -z "${HADOOP_HOME:-}" ]; then
  echo "HADOOP_HOME is not set. Please set it to the Hadoop installation directory."
  exit 1
fi

$HADOOP_HOME/bin/hdfs dfsadmin -report > ./node_report.txt || {
    echo "Failed to fetch node report. Please check if HDFS is running and HADOOP_HOME is set correctly."
    exit 1
}