#!/bin/bash

while true; do
	uptime >> $1.log;
	sleep 60;
done
