#!/usr/bin/env python3

import os


os.system("killall dd")
os.system("/opt/spark/sbin/stop-slave.sh")

