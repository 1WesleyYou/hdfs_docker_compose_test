# Classification of HDFS Open Issues

## Logging Error

| Issue ID | Version | Trigger | Explain |
|----------|---------|-----------|--------|
| 14945 | 3.1.3 | for a datanode in a pipeline, `PacketResponder` thread encounters an exception, it prints the reason wrongly | file `hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BlockReceiver.java` line 1491, the warn content should not be `BlockReceiver.run()` but `PacketResponder.run()`|


## Test

| Issue ID | Version | Trigger | Explain |
|----------|---------|-----------|--------|
