#!/usr/bin/env python3

import os

for slave in open("slaves.txt", "r"):
    os.system('scp -o "StrictHostKeyChecking no" start-slave.py '+ slave.strip() + ":")
    os.system('scp stop-slave.py '+ slave.strip() + ":")
    os.system('scp start-slave-logging.py '+ slave.strip() + ":")
    os.system('scp stop-slave-logging.py '+ slave.strip() + ":")
    os.system('scp log.sh '+ slave.strip() + ":")
