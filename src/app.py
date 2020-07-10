from flask import Flask, render_template
from fuzzer import engine
from flask_socketio import SocketIO, send, emit
import threading
import random
import json
import time
import datetime

app = Flask(__name__)
socketio = SocketIO(app)

from flask_socketio import send, emit

fuzzing = False
fuzzing_thread = None
data_thread = None

def output_collector():
    global socketio, fuzzing

    while fuzzing:
        fuzzer = engine.fuzzer_instance()

        try:
            json_data = {'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'value': fuzzer.summary_stats["execs_per_sec"]}

            socketio.emit("output", json_data)
        except:
            pass

        time.sleep(1)

@socketio.on('start_fuzzing')
def start_fuzzing(data):
    global fuzzing_thread, fuzzing

    print(f"Calling fuzzing engine with: {data}")


    fuzzing_thread = threading.Thread(target=engine.start_fuzzing, args=(
        data['binary'],
        data['afl_cores'],
        data['first_crash'],
        data['no_dictionary'],
        data['driller_cores'],))

    fuzzing = True
    fuzzing_thread.start()

    data_thread = threading.Thread(target=output_collector)
    data_thread.start()

@socketio.on('stop_fuzzing')
def stop_fuzzing(data):
    global fuzzing
    engine.stop_fuzzing()
    fuzzing = False

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8888)

    # for running without socketio
    # app.run(debug=True, host='0.0.0.0', port=8888)
