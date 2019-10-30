#!/usr/bin/env python3

import argparse
import re
import os
import time

def run(command):
    print(command)
    os.system(command)
    time.sleep(1)

def run_over_ssh(ip, command):
    print("ssh -t " + ip + " " + command)
    run("ssh -t " + ip + " " + command)

def stop_slave_logging(ip):
    command = "killall vmstat"
    run_over_ssh(ip, command)
    print("stopped slave logging " + ip)

def stop_logging():
    for slave in slaves:
        stop_slave_logging(slave)

slaves = list()

for line in open("slaves.txt", "r"):
    slaves.append(line.strip())

stop_logging()

