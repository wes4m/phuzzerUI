from flask import Flask, render_template
#from fuzzer import engine
from flask_socketio import SocketIO, send, emit
import threading
import random
import json
import time
import datetime
import sys
import os.path



app = Flask(__name__)
socketio = SocketIO(app)

from flask_socketio import send, emit

fuzzing = False
data_thread = None
logpath = None

def output_collector():
    global socketio, fuzzing, logpath

    while fuzzing:

        try:
            # dumb temporary fix
            paths = open(f"{logpath}fuzzer-master.log","r").read().split("(")[-1].split(" total")[0]
            execs = open(f"{logpath}fuzzer-master/fuzzer_stats", "r").read().split('execs_per_sec')[1].split(':')[1].split('paths_total')[0].strip()
            print(f"Execs\Paths total dumb: {execs}\{paths}")

            #json_data = {'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            #                    'value': fuzzer.summary_stats["execs_per_sec"]}
            json_data = {'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'value': execs}
            json_data_cov = {'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'value': paths}

            # non-accurate/slow stats
            # print(fuzzer.summary_stats)


            socketio.emit("output", json_data)
            socketio.emit("output-coverage", json_data_cov)

        except:
            pass

        time.sleep(1)


def fuzzing_monitor():
    global logpath, fuzzing

    while True:
        if os.path.isfile(f"{logpath}fuzzer-master.log"):
            print(f"{logpath}fuzz-master.log found, CI started fuzzing")
            fuzzing = True
        else:
            print(f"{logpath}fuzz-master.log deleted, CI finished fuzzing")
            fuzzing = False

        time.sleep(2)

def start_monitor_fuzzing(local_logpath):
    global data_thread, logpath
    logpath = local_logpath

    print(f"Starting CI fuzzing monitor with logpath {logpath}")

    threading.Thread(target=fuzzing_monitor).start()

    data_thread = threading.Thread(target=output_collector)
    data_thread.start()

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8888)
    start_monitor_fuzzing("/dev/shm/work/")
    # for running without socketio
    # app.run(debug=True, host='0.0.0.0', port=8888)
