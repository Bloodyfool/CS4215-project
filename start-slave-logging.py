#!/usr/bin/env python3

import argparse
import os
import time

parser = argparse.ArgumentParser(description="Flip a switch by setting a flag")
parser.add_argument('-n', '--name', action='store', help='name of experiment', required=True, type=str)
parser.add_argument('--id', action='store', help='ip of master', required=True, type=int)

args = parser.parse_args()

NAME=args.name
ID=str(args.id)

# os.system("sudo apt install psmisc")

os.system("nohup vmstat -t 5 > "+NAME+"_"+ID+".log &")
time.sleep(3)
