import numpy as np
import socketio
import eventlet
import base64
import cv2
import inputs
import multiprocessing
from gamepad import GamepadHandler
from gamepad import GamepadReader

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
connected_clients = ''


@sio.event
def on_connect(sid, environ):
    print(sio.emit('receiveGamepad', "HALLO",room=sid))
    print(f"Client {sid} connected.")
    sio.emit('receive', 'JALO', room=connected_clients)
    connected_clients = sid

@sio.on('stream_video')
def stream_video(sid, data):
    # Decode base64-encoded video frame
    decoded_frame = base64.b64decode(data)
    # Convert the video frame to numpy array
    nparr = np.frombuffer(decoded_frame, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    frame = cv2.resize(frame, (640, 480))
    # Show the video frame (viewer)
    cv2.imshow('Received Video', frame)
    cv2.waitKey(1)


@sio.on('disconnect')
def on_disconnect(sid):
    print(f"Client {sid} disconnected.")
    # Menghapus session ID dari dictionary saat client terputus
    if sid in connected_clients:
        del connected_clients[sid]


def running():
    global dataGamepad
    GamepadReader()
    gamepad_handler = GamepadHandler()
    while True:
        events = inputs.get_gamepad()
        for event in events:
            data = gamepad_handler.handle_event(event)
            if data == 'A':
                dataGamepad = 'B'
                print(dataGamepad)
                sio.emit('receive', data, room=connected_clients)

                
if __name__ == '__main__':
   process_gamepad = multiprocessing.Process(target=running)
   process_gamepad.start()
   eventlet.wsgi.server(eventlet.listen(('192.168.1.102', 5001)), app)


