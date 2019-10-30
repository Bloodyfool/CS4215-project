#!/usr/bin/env python3

import argparse
import re
import os
import time

def regex_type(s, pat=re.compile(r"[a-f0-9A-F]{32}")):
    if not pat.match(s):
        raise argparse.ArgumentTypeError
    return s

def ip_address(s):
    return regex_type(s, pat=re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"))

parser = argparse.ArgumentParser(description="Flip a switch by setting a flag")
parser.add_argument('-m', '--master', action='store', help='ip of master', required=True, type=ip_address)
parser.add_argument('-c', '--cpu', action='store', help='fraction of cpu to use for fast machines', required=True, type=float)
parser.add_argument('-r', '--ram', action='store', help='gigs of ram to give to a fast worker', required=True, type=int)
parser.add_argument('-f', '--fast', action='store', help='number of nodes to make fast', required=True, type=int)

args = parser.parse_args()

MASTER=args.master
CPU=str(int((1-args.cpu)*100))
MEMORY=str(args.ram)
N_FAST=int(args.fast)

def run(command):
    print(command)
    os.system(command)
    time.sleep(1)

def run_over_ssh(ip, command):
    print("ssh -t " + ip + " " + command)
    run("ssh -t " + ip + " " + command)
    # print(command)
    # run(command)
    # print()

def start_slave(ip, master, cpu, mem):
    print("starting slave " + ip)
    command = "./start-slave.py -m "+master+" -c "+cpu+" -r "+mem
    run_over_ssh(ip, command)
    print("started slave " + ip)
    print()

def stop_slave(ip):
    command = "./stop-slave.py"
    run_over_ssh(ip, command)
    print("stopped slave " + ip)

def stop_slaves():
    for slave in slaves:
        stop_slave(slave)

def start_master(master, memory):
    os.system("""sudo sed -i 's/"master": "spark:.*$/"master": "spark:\/\/"""+master+""":7077",/' /home/test/bd/sparkgen-bigdl/conf.json.sample""")
    time.sleep(1)
    os.system("""sudo sed -i 's/"totalExecutorCores": ".*$/"totalExecutorCores": "4",/' /home/test/bd/sparkgen-bigdl/conf.json.sample""")
    time.sleep(1)
    os.system("""sudo sed -i 's/"executorMemory": ".*$/"executorMemory": \""""+memory+"""G",/' /home/test/bd/sparkgen-bigdl/conf.json.sample""")
    time.sleep(1)
    os.system("sudo rm /home/test/bd/sparkgen-bigdl/bigdl.log")
    time.sleep(1)
    run('sudo su -c "/home/test/bd/spark/sbin/start-master.sh -h '+master+'" test')

def stop_master():
    run('sudo su -c "/home/test/bd/spark/sbin/stop-master.sh" test')

def start_spark(master, cpu, memory, n_fast):
    stop_master()
    stop_slaves()
    start_master(master, memory)
    for idx, slave in enumerate(slaves):
        if idx < n_fast:
            print("Starting fast slave")
            start_slave(slave, master, cpu, memory)
        else:
            print("Starting slow slave")
            start_slave(slave, master, "75", memory)

slaves = list()

for line in open("slaves.txt", "r"):
    slaves.append(line.strip())

start_spark(MASTER, CPU, MEMORY, N_FAST)

