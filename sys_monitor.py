#!/usr/bin/env python3
# This script is used to monitor system metrics such as user info, memory usage, disk usage, and network speed.
# All metrics are within the local system, not connectivity with other nodes.

import os
import psutil
import time
from loguru import logger
import datetime
import sys
import glob
import json
import subprocess

def view_user():
    logger.debug("User Info:")
    for user in psutil.users():
        logger.info(user.name)
    logger.info(
        "System Time: Boot Time: {}, Running Time: {}",
        psutil.boot_time(),
        datetime.datetime.fromtimestamp(psutil.boot_time()),
    )


def view_mem():
    # read virtual memory info
    vm = psutil.virtual_memory()
    logger.info(
        "Virtual Memory Info: Total: {}; Available: {}; Used: {}; Free: {}; Percent: {}%; "
        "Active: {}; Inactive: {}; Buffers: {}; Cached: {}",
        vm.total,
        vm.available,
        vm.used,
        vm.free,
        vm.percent,
        vm.active,
        vm.inactive,
        vm.buffers,
        vm.cached,
    )

    # read swap memory info
    # logger.info(f"Swap Memory Info: {psutil.swap_memory()}")
    sm = psutil.swap_memory()

    logger.info(
        "Swap Memory Info: Total: {}; Used: {}; Free: {}; Percent: {}; Sin: {}; Sout: {}",
        sm.total,
        sm.used,
        sm.free,
        sm.percent,
        sm.sin,
        sm.sout,
    )


def view_disk(interval=1):
    logger.debug("Disk Usage Info:")
    for disk in psutil.disk_partitions():
        if disk.mountpoint.startswith("/boot"):
            continue
        usage = psutil.disk_usage(disk.mountpoint)
        logger.info(
            "Disk: {}, Mountpoint: {}, Fstype: {}, Options: {}\n"
            "       Usage: total={}B, used={}B, free={}B, percent={}%",
            disk.device,
            disk.mountpoint,
            disk.fstype,
            disk.opts,
            usage.total,
            usage.used,
            usage.free,
            usage.percent,
        )

    io_before = psutil.disk_io_counters(perdisk=True)

    time.sleep(interval)

    io_after = psutil.disk_io_counters(perdisk=True)

    logger.debug("Disk Throughput over {}s:", interval)
    for dev, before in io_before.items():
        if dev.startswith("loop"):
            continue
        after = io_after.get(dev)
        if not after:
            continue

        delta_read_bytes = after.read_bytes - before.read_bytes
        delta_write_bytes = after.write_bytes - before.write_bytes
        delta_read_cnt = after.read_count - before.read_count
        delta_write_cnt = after.write_count - before.write_count

        read_bps = delta_read_bytes / interval
        write_bps = delta_write_bytes / interval
        read_ops = delta_read_cnt / interval
        write_ops = delta_write_cnt / interval

        logger.info(
            "Disk {}: Read {:.2f} B/s ({} ops/s), Write {:.2f} B/s ({} ops/s)",
            dev,
            read_bps,
            read_ops,
            write_bps,
            write_ops,
        )


def view_network(interval=1):
    logger.debug("Start Measuring Network Speed")
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()

    sent_per_s = (net2.bytes_sent - net1.bytes_sent) / interval
    recv_per_s = (net2.bytes_recv - net1.bytes_recv) / interval
    pkt_sent_ps = (net2.packets_sent - net1.packets_sent) / interval
    pkt_recv_ps = (net2.packets_recv - net1.packets_recv) / interval
    errin_delta = net2.errin - net1.errin
    errout_delta = net2.errout - net1.errout
    dropin_delta = net2.dropin - net1.dropin
    dropout_delta = net2.dropout - net1.dropout

    logger.info(
        "Network over {}s: Sent {:.2f} B/s ({:.2f} pkt/s), Recv {:.2f} B/s ({:.2f} pkt/s), "
        "Err In {} Out {}, Drop In {} Out {}",
        interval,
        sent_per_s,
        pkt_sent_ps,
        recv_per_s,
        pkt_recv_ps,
        errin_delta,
        errout_delta,
        dropin_delta,
        dropout_delta,
    )


def view_hdfs_log():
    hadoop_home = os.getenv("HADOOP_HOME")    
    if not hadoop_home:
        # logger.error("HADOOP_HOME environment variable is not set.")
        print("[\033[31mERROR\033[0m] HADOOP_HOME environment variable is not set.")
        sys.exit(1)

    log_dir = os.path.join(hadoop_home, "logs")
    if not os.path.isdir(log_dir):
        print(f"[\033[31mERROR\033[0m] Hadoop log directory {log_dir} does not exist.")
        sys.exit(1)

    pattern = os.path.join(log_dir, "*.log") 
    log_files = glob.glob(pattern)
    if not log_files:
        print(f"[\033[31mERROR\033[0m] No log files found in {log_dir}.")
        sys.exit(1)
    
    script_path = "./tail_hadoop.sh"
    output_file = "hdfs.log"

    try:
        with open(output_file, "w") as f:
            subprocess.run(
                [script_path],
                stdout=f,
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )
            print(f"[\033[32mSUCCESS\033[0m] HDFS logs written to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"[\033[31mERROR\033[0m] Failed to run {script_path}: {e.stderr.strip()}")
        sys.exit(1)

def view_hdfs_report():
    hadoop_home = os.getenv("HADOOP_HOME")    
    if not hadoop_home:
        # logger.error("HADOOP_HOME environment variable is not set.")
        print("[\033[31mERROR\033[0m] HADOOP_HOME environment variable is not set.")
        sys.exit(1)
    log_dir = os.path.join(hadoop_home, "logs")
    if not os.path.isdir(log_dir):
        print(f"[\033[31mERROR\033[0m] Hadoop log directory {log_dir} does not exist.")
        sys.exit(1)

    pattern = os.path.join(log_dir, "*.log") 
    log_files = glob.glob(pattern)
    if not log_files:
        print(f"[\033[31mERROR\033[0m] No log files found in {log_dir}.")
        sys.exit(1)
    
    script_path = "./hdfs_16633/fetchNodeReport.sh"

    try:
        subprocess.run(
            [script_path],
        )
        print(f"[\033[32mSUCCESS\033[0m] HDFS logs written to node_report.txt.")
    except subprocess.CalledProcessError as e:
        print(f"[\033[31mERROR\033[0m] Failed to run {script_path}: {e.stderr.strip()}")
        sys.exit(1)

# sysMonitor = SystemMonitor(g g
if __name__ == "__main__":
    logger.remove()
    # logger.add(sys.stdout, format="{message}", serialize=True, level="DEBUG")
    logger.add(
        "sysMetric.json",
        rotation="10 MB",
        retention="7 days",
        serialize=True,
        level="INFO",
    )

    # logger.debug("This is a debug, won't be in app.json")
    view_user()
    view_mem()
    view_disk()
    view_network()
    view_hdfs_log()
    view_hdfs_report()
