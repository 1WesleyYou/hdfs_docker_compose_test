#!/usr/bin/env python3

import os
import psutil
import time
from loguru import logger
import datetime


def view_user():
    logger.debug("User Info:")
    for user in psutil.users():
        logger.info(user.name)
    logger.debug("System Time:")
    logger.info("Boot Time: {}", psutil.boot_time())
    logger.info("Running Time: {}", datetime.datetime.fromtimestamp(psutil.boot_time()))


def view_mem():
    # read virtual memory info
    vm = psutil.virtual_memory()
    logger.debug("Virtual Memory Info:")
    # logger.info(f"Virtual Memory Info: {psutil.virtual_memory()}")
    logger.info("Total: {};  Avail: {};  Percent: {}", vm.total, vm.available, vm.percent, vm.used)
    logger.info("Used: {};    Free: {};", vm.used, vm.free)
    logger.info("Active: {}; Inactive: {};", vm.active, vm.inactive)
    logger.info("Buffers: {}; Cached: {};", vm.buffers, vm.cached)

    # read swap memory info
    # logger.info(f"Swap Memory Info: {psutil.swap_memory()}")
    sm = psutil.swap_memory()
    logger.debug("Swap Memory Info:")
    logger.info("Total: {};  Used: {};  Free: {}", sm.total, sm.used, sm.free)
    logger.info("Percent: {};  Sin: {};  Sout: {}", sm.percent, sm.sin, sm.sout)


def view_disk(interval=1):
    logger.debug("Disk Usage Info:")
    for disk in psutil.disk_partitions():
        if disk.mountpoint.startswith('/boot'):
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
            usage.percent
        )

    io_before = psutil.disk_io_counters(perdisk=True)

    time.sleep(interval)

    io_after = psutil.disk_io_counters(perdisk=True)

    logger.debug("Disk Throughput over {}s:", interval)
    for dev, before in io_before.items():
        if dev.startswith('loop'):
            continue
        after = io_after.get(dev)
        if not after:
            continue

        delta_read_bytes  = after.read_bytes   - before.read_bytes
        delta_write_bytes = after.write_bytes  - before.write_bytes
        delta_read_cnt    = after.read_count   - before.read_count
        delta_write_cnt   = after.write_count  - before.write_count

        read_bps  = delta_read_bytes  / interval
        write_bps = delta_write_bytes / interval
        read_ops  = delta_read_cnt    / interval
        write_ops = delta_write_cnt   / interval

        logger.info(
            "Disk {}: Read {:.2f} B/s ({} ops/s), Write {:.2f} B/s ({} ops/s)",
            dev,
            read_bps,
            read_ops,
            write_bps,
            write_ops
        )

def view_network(interval=1):
    logger.debug("Start Measuring Network Speed")
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()

    sent_per_s   = (net2.bytes_sent   - net1.bytes_sent)   / interval
    recv_per_s   = (net2.bytes_recv   - net1.bytes_recv)   / interval
    pkt_sent_ps  = (net2.packets_sent - net1.packets_sent) / interval
    pkt_recv_ps  = (net2.packets_recv - net1.packets_recv) / interval
    errin_delta  = net2.errin   - net1.errin
    errout_delta = net2.errout  - net1.errout
    dropin_delta = net2.dropin  - net1.dropin
    dropout_delta= net2.dropout - net1.dropout

    logger.debug("Network speed over {}s:", interval)
    logger.info("Bytes Sent:   {:.2f} B/s", sent_per_s)
    logger.info("Bytes Recv:   {:.2f} B/s", recv_per_s)
    logger.info("Packets Sent: {:.2f} pkt/s", pkt_sent_ps)
    logger.info("Packets Recv: {:.2f} pkt/s", pkt_recv_ps)
    logger.info("Errors In:    {}", errin_delta)
    logger.info("Errors Out:   {}", errout_delta)
    logger.info("Dropped In:   {}", dropin_delta)
    logger.info("Dropped Out:  {}", dropout_delta)

# sysMonitor = SystemMonitor()
if __name__ == "__main__":
    view_user()
    view_mem()
    view_disk()
    view_network()