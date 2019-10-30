#!/usr/bin/env python3

import argparse
import os
import time

parser = argparse.ArgumentParser(description="Flip a switch by setting a flag")
parser.add_argument('-n', '--name', action='store', help='name of experiment', required=True, type=str)

args = parser.parse_args()

NAME=args.name

os.system("mkdir -p " + NAME)
time.sleep(1)

for slave in open("slaves.txt", "r"):
    os.system("scp "+slave.strip()+":"+NAME+"* " + NAME)
    time.sleep(1)

