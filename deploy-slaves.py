#!/usr/bin/env python3

import os
import time

for slave in open("slaves.txt", "r"):
    os.system('scp -o "StrictHostKeyChecking no" start-slave.py '+ slave.strip() + ":")
    time.sleep(1)
    os.system('scp stop-slave.py '+ slave.strip() + ":")
    time.sleep(1)
    os.system('scp start-slave-logging.py '+ slave.strip() + ":")
    time.sleep(1)
    os.system('scp stop-slave-logging.py '+ slave.strip() + ":")
    time.sleep(1)
    os.system('scp log.sh '+ slave.strip() + ":")
    time.sleep(1)
