#!/usr/bin/env python3

import os
import time

os.system("killall dd")
os.system("/opt/spark/sbin/stop-slave.sh")
time.sleep(1)

