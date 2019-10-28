#!/usr/bin/env python3

import os

def run_over_ssh(ip, command):
    print("ssh -t " + ip + " " + command)
    run("ssh -t " + ip + " " + command)

def stop_slave(ip):
    command = "./stop-slave.py"
    run_over_ssh(ip, command)
    print("stopped slave " + ip)

def stop_slaves():
    for slave in slaves:
        stop_slave(slave)

def stop_master():
    run('sudo su -c "/home/test/bd/spark/sbin/stop-master.sh" test')

def stop_spark():
    stop_master()
    stop_slaves()

slaves = list()

for line in open("slaves.txt", "r"):
    slaves.append(line.strip())

stop_spark()

