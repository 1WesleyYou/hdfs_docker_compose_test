# Hadoop Distributed File System Open Issue \#16633 Reproduction

This folder refers to the install and trigger code in the project [T2C](https://github.com/OrderLab/T2C/tree/main/experiments/detection/hdfs/HDFS16633)

And all codes are tested on Ubuntu 22.04 LTS

## Usage

The basic structure of the folder is like the following

```bash
hdfs_16633/
├── core-site.xml  # for hdfs cfg
├── hdfs_16633_install.sh  # build hadoop (clone first)
├── hdfs-16633.patch  # used to fix up small issues 
├── hdfs-site.xml  # for hdfs cfg
├── README.md
├── setup.sh  # first script to run
└── trigger.sh  # trigger issue from built hadoop
```

To reproduce the same problem, you could follow the order below:

1. `bash setup.sh`, this will install necessary packages (including the protoc) for the system. This step roughly takes 5min.
2. `git clone https://github.com/apache/hadoop.git` to clone the 
3. `chmod +x hdfs_16633_install.sh` and then `./hdfs_16633_install.sh ../hadoop`, the latter part `../hadoop` is the path from workspace to the cloned apache hadoop directory.
4. `chmod +x trigger.sh` and then `./trigger.sh ../hadoop`