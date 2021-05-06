'''
FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
'''

from flask_socketio import SocketIO, emit
from flask import Flask,Response, render_template, url_for, copy_current_request_context

from threading import Thread, Event

"""
Flask handler manages the start and connection to Flask website/server.
"""

from file_handler import ConfigHandler

app = Flask(__name__, static_url_path='/static')
app.config['DEBUG'] = False # let this be false to only start one webbrowser
app.config['THREADED'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode="threading")

thread = Thread() # scheduler thread
thread_stop_event = Event()

def start_flask_application(shared):
    [HOST,PORT] = ConfigHandler().get_all("Flask") # pylint: disable=unbalanced-tuple-unpacking
    socketio.run(app, host=HOST, port=PORT) # SocketIOServer
    app.run(host=HOST, port=PORT) # Other Server

@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

# TODO add view model and image
vcapture_list = []
def gen(device):
    import cv2
    try:
        if(device in vcapture_list):
            print("Device stream already streaming " + str(device))
        vcap = cv2.VideoCapture(device)
        vcapture_list.append(device)
        while True:
            ret, frame = vcap.read()
            if frame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')
    except Exception:
        print("Capture failed " + str(device))

@app.route('/video_feed/<device>')
def video_feed(device):
    # return the response generated along with the specific media
    # type (mime type)
    print(device)
    device = device.replace("skipableslash","/")
    print(device)
    try:
        return Response(gen(int(device)),mimetype = "multipart/x-mixed-replace; boundary=frame")
    except Exception:
        return Response(gen(device),mimetype = "multipart/x-mixed-replace; boundary=frame")

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Flask Client connected')

    #Start the generator threads only if the thread has not been started before.
    if not thread.isAlive():
        #scheduler()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Flask Client disconnected')