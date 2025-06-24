# run this script on the server, reproducing HDFS16633 only need one server
# $1 should be the directory of Hadoop source code
cd $1
version='3.1.2'
cd hadoop-dist/target/hadoop-${version}/
rm -rf /tmp/hadoop-yuchenxr/dfs/data/  # clean up the data node history
./bin/hdfs namenode -format
./bin/hdfs --daemon start namenode
./bin/hdfs --daemon start datanode
# ./sbin/hadoop-daemon.sh start namenode
# ./sbin/hadoop-daemon.sh start datanode
echo "sleep 8 seconds"
sleep 8
echo "running work load"
./bin/hadoop org.apache.hadoop.hdfs.NNBenchWithoutMR -operation createWrite -baseDir /benchmarks -numFiles 100 -blocksPerFile 16 -bytesPerBlock 1048576
sleep 3
echo "now there should be messages 'ERROR org.apache.hadoop.hdfs.server.datanode.DataNode: ubuntu:9866:DataXceiver error processing WRITE_BLOCK operation' and 'CHANG: inject IOException!' in logs/hadoop-username-datanode-hostname.log" 
echo "now the issue is reproduced"
./bin/hdfs --daemon stop datanode
./bin/hdfs --daemon stop namenode
# ./sbin/hadoop-daemon.sh stop datanode
# ./sbin/hadoop-daemon.sh stop namenode