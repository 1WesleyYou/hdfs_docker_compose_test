# Classification of HDFS Open Issues

## Logging Error

| Issue ID | Version | Trigger | Explain |
|----------|---------|-----------|--------|
| 14945 | 3.1.3 | for a datanode in a pipeline, `PacketResponder` thread encounters an exception, it prints the reason wrongly | file `hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BlockReceiver.java` line 1491, the warn content should not be `BlockReceiver.run()` but `PacketResponder.run()`|

## Test

| Issue ID | Version | Trigger | Explain |
|----------|---------|-----------|--------|
| 14958 | 3.1.3 | `CommonConfigurationKeysPlublic.NET_TOPOLOGY_IMPL_KEY` is ignored and the test actually uses the default `DFSNetworkTopology`| The flag `DFSConfigKeys.DFS_SUE_NETWORK_TOPOLOGY_KEY` default to true, and thus the `Common...` flag is ignored |

## Erasure Coding Recovery

| Issue ID | Version | Trigger | Description | 
|------------|---------|------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| 15186 | 3.1.3 | Simultaneous decommission of multiple DataNodes in an EC-enabled cluster | Duplicate `targetIndices` in `StripedReconstructionInfo` cause the EC decoder to treat a source index as a target, producing parity blocks full of zeros |

## Downgrade Compatibility

| Issue ID | Version | Trigger | Description | Resolution |
|------------|---------|---------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 14831 | 3.1.3 | Downgrading from Hadoop 3.2.0 down to 2.7.x | Incompatible changes to the FSImage `StringTable` (commit `8a41edb089fbdedc5e7d9a2aeec63d126afea49f`) prevent a 2.7.x NameNode from reading a 3.x fsimage, causing startup failure :contentReference[oaicite:1]{index=1} | Revert or back‐port the `StringTable` format change (apply commit `8a41edb089fbdedc5e7d9a2aeec63d126afea49f`) so that older NameNodes can read the image (see HDFS-13596), or upgrade to a release that includes this fix :contentReference[oaicite:2]{index=2}. |
