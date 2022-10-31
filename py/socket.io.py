from ast import arg
from time import sleep
import socketio

# standard Python
sio = socketio.Client()
sio.connect('http://localhost:8000')

sio.emit('pair', {'foo': 'bar'})
sleep(3)
# sio.wait()
sio.disconnect()