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
# current = db[meeting["meeting_official_name"]]
current = db["FORMULA 1 QATAR AIRWAYS AUSTRIAN GRAND PRIX 2024"]
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
        try:
            compiled={}
            standingsdict=current.find_one({"Type":"standings"})
            print("abc",standingsdict)
            standingsint=standingsdict['Standings']
            standings=[]
            for i in standingsint:
                standings.append(str(i))
            compiled['standings']=",".join(standings)
            for n in range(len(standings)):
                #print(standingsint)
                #print(n)
                a=current.find_one({'Type':'driver','Number':standingsint[n]})
                try:
                    b=a['Info'].values()
                    c=[]
                    for d in b:
                        if isinstance(d,int):
                            c.append(str(d))
                        else:
                            c.append(d)
                    compiled["P"+str(n+1)]=",".join(c)
                except:
                    pass
            a=len(standings)
            while a < 20:
                compiled["P"+str(a+1)]=",".join([404,"NA"])
                a=a+1
            socketio.emit('my_response', compiled)
            print("Success")
        except Exception as e:
            print("hello", e)
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
    socketio.run(app, debug=True)