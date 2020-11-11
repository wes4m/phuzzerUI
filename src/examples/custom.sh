#!/bin/sh

/usr/bin/afl-unix/afl-fuzz -i /dev/shm/work/initial_seeds -o /dev/shm/work/ -m 8G -M fuzzer-master -x DICT ARGS BIN > /dev/shm/work/fuzzer-master.log
