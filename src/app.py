from flask import Flask, render_template
from fuzzer import engine
from flask_socketio import SocketIO, send, emit
import threading

app = Flask(__name__)
socketio = SocketIO(app)

from flask_socketio import send, emit

fuzzing_thread = None

@socketio.on('start_fuzzing')
def start_fuzzing(data):
    global fuzzing_thread

    print(f"Calling fuzzing engine with: {data}")


    fuzzing_thread = threading.Thread(target=engine.start_fuzzing, args=(
        data['binary'],
        data['afl_cores'],
        data['first_crash'],
        data['no_dictionary'],))

    fuzzing_thread.start()


@socketio.on('stop_fuzzing')
def stop_fuzzing(data):
    engine.stop_fuzzing()

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8888)

    # for running without socketio
    # app.run(debug=True, host='0.0.0.0', port=8888)
