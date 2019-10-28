#!/usr/bin/env python3

import argparse
import re
import os

def regex_type(s, pat=re.compile(r"[a-f0-9A-F]{32}")):
    if not pat.match(s):
        raise argparse.ArgumentTypeError
    return s

def ip_address(s):
    return regex_type(s, pat=re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"))

def run(command):
    # print(command)
    os.system(command)

parser = argparse.ArgumentParser(description="Flip a switch by setting a flag")
parser.add_argument('-m', '--master', action='store', help='ip of master', required=True, type=ip_address)
parser.add_argument('-c', '--cpu', action='store', help='fraction of cpu to use', required=True, type=int)
parser.add_argument('-r', '--ram', action='store', help='gigs of ram to give to the worker', required=True, type=int)

args = parser.parse_args()

MASTER=args.master
CPU=str(args.cpu)
MEMORY=str(args.ram)

run("killall dd")
run("/opt/spark/sbin/stop-slave.sh")
run("rm -r /opt/spark/work/*")

run("/opt/spark/sbin/start-slave.sh spark://"+MASTER+":7077 -m "+MEMORY+"G")

if(CPU != "0"):
    run("cpulimit -l "+CPU+" dd if=/dev/zero of=/dev/null &")

