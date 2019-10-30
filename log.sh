#!/bin/bash

while true; do
	echo $(date +%s) $(uptime) >> $1.log;
	sleep 5;
done
