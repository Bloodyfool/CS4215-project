#!/usr/bin/env python3

import argparse
import os
import time

parser = argparse.ArgumentParser(description="Flip a switch by setting a flag")
parser.add_argument('-n', '--name', action='store', help='ip of master', required=True, type=str)

args = parser.parse_args()

NAME=args.name

def run(command):
    print(command)
    os.system(command)
    time.sleep(1)

def run_over_ssh(ip, command):
    print("ssh -t " + ip + " " + command)
    run("ssh -t " + ip + " " + command)

def start_slave_logging(ip, idx, name):
    command = "./start-slave-logging.py --id " + str(idx) + " -n " + name
    run_over_ssh(ip, command)
    print("started slave logging" + ip)

def start_logging(name):
    for idx, slave in enumerate(slaves, start=1):
        start_slave_logging(slave, idx, name)

slaves = list()

for line in open("slaves.txt", "r"):
    slaves.append(line.strip())

start_logging(NAME)

