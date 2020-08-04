#!/bin/bash

# Sets kernel options for AFL
echo core > /proc/sys/kernel/core_pattern
echo 1 > /proc/sys/kernel/sched_child_runs_first


# install deps (everytime it runs, intentional to avoid rebuilding the container for UI updates)
echo "Installing WebUI dependencies .."
pip3 install -r requirements.txt


# initial seeds and fuzzer files
cp -r /phuzzui/examples/work /dev/shm/

# run
python3 app.py

