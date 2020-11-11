#!/bin/sh

/usr/bin/afl-unix/afl-fuzz -i /dev/shm/work/initial_seeds -o /dev/shm/work/ -m 8G -M fuzzer-master -x /dev/shm/work/dict.txt -- /phuzzui/examples/mavlink > /dev/shm/work/fuzzer-master.log
