/usr/bin/afl-unix/afl-fuzz -i /dev/shm/work/initial_seeds -o /dev/shm/work/ -m 8G -Q -M fuzzer-master -x /dev/shm/work/dict.txt -- /phuzzui/examples/example-elf
