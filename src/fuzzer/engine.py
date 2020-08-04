import os
import imp
import time
import shutil
import socket
import driller
import tarfile
import argparse
import importlib
import logging.config
import subprocess

from phuzzer import AFL
from phuzzer import GreaseCallback

fuzzer = None
fuzzing = None
process = None

def fuzzer_instance():
    global fuzzer
    return fuzzer

def stop_fuzzing():
    global fuzzer, fuzzing, process
    if fuzzing:
        fuzzer.stop()

    if process is not None:
        process.terminate()

def start_mavlink_AFL():
    global process

    print(f"[*] Starting AFL for mavlink")
    process = subprocess.Popen(['/phuzzui/examples/mavlink_afl.sh'])


# Quick stripped example
# Based on phuzzer's __main__.py
def start_fuzzing(fpath, fafl_cores, ffirst_crash, fno_dictionary, drillers):
    global fuzzer, fuzzing

    # "the path to the target binary to fuzz"
    binary = fpath
    # The logging configuration file.", default=".shellphuzz.ini"
    logcfg = ".shellphuzz.ini"
    # "A module that includes some helper scripts for seed selection and such."
    helper_module = None
    # "When the fuzzer gets stuck, drill with N workers."
    drill_extension = drillers
    # "A directory of inputs to grease the fuzzer with when it gets stuck."
    grease_extension = None
    # "Directory of files to seed fuzzer with"
    seeds = [b"/phuzzui/fuzzer/seeds"]
    # "Number of AFL workers to spin up.", default=1
    afl_cores = fafl_cores
    # "The work directory for AFL.", default="/dev/shm/work/"
    work_dir = "/dev/shm/work/"
    # "Force greaser/fuzzer assistance at a regular interval (in seconds)."
    force_interval = None
    # "Do not create a dictionary before fuzzing.",  default=False
    no_dictionary = fno_dictionary
    # help="Timeout (in seconds)."
    timeout = None
    # "Memory limit to pass to AFL (MB, or use k, M, G, T suffixes)", default="8G"
    memory = "8G"
    # "Number of seconds permitted for each run of binary"
    run_timeout = None
    # help="Stop on the first crash.", default=False
    first_crash = ffirst_crash
    # Qemu mode or instrumnted (Default instrumntation mode)
    use_qemu = False

    if os.path.isfile(os.path.join(os.getcwd(), logcfg)):
        logging.config.fileConfig(os.path.join(os.getcwd(), logcfg))

    try: os.mkdir("/dev/shm/work/")
    except OSError: pass

    stuck_callback = (
        (lambda f: (grease_extension(f), drill_extension(f))) if drill_extension and grease_extension
        else drill_extension or grease_extension
    )

    print ("[*] Creating fuzzer...")
    fuzzer = AFL(
        binary, work_dir=work_dir, seeds=seeds, afl_count=afl_cores,
        create_dictionary=not no_dictionary, timeout=timeout,
        memory=memory, run_timeout=run_timeout, use_qemu=False ,
    )

    print ("[*] Starting fuzzer...")
    fuzzer.start()
    start_time = time.time()

    try:
        crash_seen = False
        while True:
            elapsed_time = time.time() - start_time
            status_str = build_status_str(elapsed_time, first_crash,timeout, afl_cores, fuzzer)
            print(status_str, end="\r")
            time.sleep(1)
            if not crash_seen and fuzzer.found_crash():
                print ("\n[*] Crash found!")
                crash_seen = True
                if first_crash:
                    break
            if fuzzer.timed_out():
                print ("\n[*] Timeout reached.")
                break

    except KeyboardInterrupt:
        print ("\n[*] Aborting wait. Ctrl-C again for KeyboardInterrupt.")
    except Exception as e:
        print ("\n[*] Unknown exception received (%s). Terminating fuzzer." % e)
        fuzzer.stop()
        if drill_extension:
            drill_extension.kill()
        raise

    print ("[*] Terminating fuzzer.")
    fuzzer.stop()
    if drill_extension:
        drill_extension.kill()



def build_status_str(elapsed_time, first_crash, timeout, afl_cores, fuzzer):
    run_until_str = ""
    timeout_str = ""
    if timeout:
        if first_crash:
            run_until_str = "until first crash or "
        run_until_str += "timeout "
        timeout_str = "for %d of %d seconds " % (elapsed_time, timeout)
    elif first_crash:
        run_until_str = "until first crash "
    else:
        run_until_str = "until stopped by you "

    summary_stats = fuzzer.summary_stats

    return "[*] %d fuzzers running %s%scompleted %d execs at %d execs/sec with %d crashes)." % \
           (afl_cores, run_until_str, timeout_str, summary_stats["execs_done"], summary_stats["execs_per_sec"],
            summary_stats["unique_crashes"])
