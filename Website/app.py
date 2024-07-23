from urllib.request import urlopen
import json
from flask import Flask, render_template, request, redirect, flash, session
from flask_socketio import SocketIO, emit
import pymongo
import time
import datetime
import certifi
from passlib.hash import pbkdf2_sha256
from threading import Lock
import requests
uri = "mongodb+srv://zahaanbatliboi:6rlwOJTWbstjuEDA@cluster0.jxt8hhc.mongodb.net/?retryWrites=true&w=majority"
cluster = pymongo.MongoClient(uri,tlsCAFile=certifi.where())
db = cluster["F1data"]
response = urlopen('https://api.openf1.org/v1/meetings?meeting_key=latest')
meeting=json.loads(response.read().decode('utf-8'))[0]
current = db[meeting["meeting_official_name"]]
app=Flask(__name__)
app.secret_key="hgsyafdysg"
import fastf1


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

url = 'https://api.coinbase.com/v2/prices/btc-usd/spot'

def background_thread():
    global current
    """Example of how to send server generated events to clients."""
    while True:
        compiled={}
        standingsdict=current.find_one({"Type":"standings"})
        standings=standingsdict['Standings']
        compiled['standings']=",".join(standings)
        for n in range(len(standings)):
            a=current.find_one({'Type':'driver','Number':n})
            if(a!=None):   
                compiled[str(n)]=",".join(a['Info'].values())
            else:
                compiled[str(n)]='Bug'
        socketio.emit('my_response', compiled)
@app.route('/')
def index():
    global current
    response = urlopen('https://api.openf1.org/v1/meetings?meeting_key=latest')
    meeting=json.loads(response.read().decode('utf-8'))[0]
    current = db[meeting["meeting_official_name"]]
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})

if __name__ == '__main__':
    socketio.run(app)