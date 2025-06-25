#!/usr/bin/env bash

set -euo pipefail

if [ -z "${HADOOP_HOME:-}" ]; then
  echo "HADOOP_HOME is not set. Please set it to the Hadoop installation directory."
  exit 1
fi

HADOOP_BIN="$HADOOP_HOME/bin/hdfs"
if [ ! -x "$HADOOP_BIN" ]; then
    echo "Hadoop binary not found or not executable: $HADOOP_BIN"
    exit 1
fi

ipc_addr=$($HADOOP_HOME/bin/hdfs getconf -confKey dfs.datanode.ipc.address)
echo "DataNode IPC Address: $ipc_addr"

$HADOOP_HOME/bin/hdfs dfsadmin -triggerBlockReport $ipc_addr || {
    echo "Failed to trigger block report. Please check if HDFS is running and HADOOP_HOME is set correctly."
    exit 1
}