#! /bin/bash
# run this scripts on the server, reproducing HDFS16633 only need one server
# version: 3.1.2
# $1 should be the directory of Hadoop source code
script_dir=$( dirname -- "$( readlink -f -- "$0"; )"; )

cd "$1" || exit 1
version='3.1.2'
git checkout tags/rel/release-$version
git apply $script_dir/hdfs-16633.patch  # only execute this line once
mvn clean package -Pdist -DskipTests -Dmaven.javadoc.skip=true -Dtar
cp $script_dir/core-site.xml hadoop-dist/target/hadoop-${version}/etc/hadoop/
cp $script_dir/hdfs-site.xml hadoop-dist/target/hadoop-${version}/etc/hadoop/
# configure JAVA_HOME in hadoop-env.sh
sed -i 's/# export JAVA_HOME=/export JAVA_HOME=\/usr\/lib\/jvm\/java-1.8.0-openjdk-amd64\//g' hadoop-dist/target/hadoop-${version}/etc/hadoop/hadoop-env.sh

sed -i '/export JAVA_HOME=/i\
export HDFS_DATANODE_OPTS="$HDFS_DATANODE_OPTS \
-Dcom.sun.management.jmxremote \
-Dcom.sun.management.jmxremote.port=9864 \
-Dcom.sun.management.jmxremote.rmi.port=9864 \
-Dcom.sun.management.jmxremote.local.only=false \
-Dcom.sun.management.jmxremote.authenticate=false \
-Dcom.sun.management.jmxremote.ssl=false"' \
hadoop-dist/target/hadoop-${version}/etc/hadoop/hadoop-env.sh

sed -i '/export JAVA_HOME=/a\
export HDFS_NAMENODE_OPTS="$HDFS_NAMENODE_OPTS \
-Dcom.sun.management.jmxremote \
-Dcom.sun.management.jmxremote.port=9999 \
-Dcom.sun.management.jmxremote.rmi.port=9999 \
-Dcom.sun.management.jmxremote.local.only=false \
-Dcom.sun.management.jmxremote.authenticate=false \
-Dcom.sun.management.jmxremote.ssl=false"' \
hadoop-dist/target/hadoop-${version}/etc/hadoop/hadoop-env.sh

# export HADOOP_HOME=$(pwd)/hadoop-dist/target/hadoop-${version}
# export HDFS_NAMENODE_OPTS="$HDFS_NAMENODE_OPTS \
#   -Dcom.sun.management.jmxremote \
#   -Dcom.sun.management.jmxremote.authenticate=false \
#   -Dcom.sun.management.jmxremote.ssl=false \
#   -Dcom.sun.management.jmxremote.portV k8004"