from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random
import pymongo
import json
from urllib.request import urlopen
import pymongo
import time
import datetime
import certifi
from passlib.hash import pbkdf2_sha256
from threading import Lock
import requests
app=Flask(__name__)
app.secret_key="H#LL0!!!!!"
socketio = SocketIO(app)

uri = "mongodb+srv://zahaanbatliboi:6rlwOJTWbstjuEDA@cluster0.jxt8hhc.mongodb.net/?retryWrites=true&w=majority"
cluster = pymongo.MongoClient(uri,tlsCAFile=certifi.where())
db = cluster["F1data"]
response = urlopen('https://api.openf1.org/v1/meetings?meeting_key=latest')
meeting=json.loads(response.read().decode('utf-8'))[0]
# current = db[meeting["meeting_official_name"]]
current = db["FORMULA 1 QATAR AIRWAYS AUSTRIAN GRAND PRIX 2024"]

@app.route('/')
def index():
    return render_template("home.html")

# @app.route('/update', methods=["GET", "POST"])
# def update():
#     if(request.method == "GET"):
#         return render_template("update.html")

#     if(request.method == "POST"):
#         racedata={"driver":"ALB","pos":"1","random":str(random.randint(1,100))}
#         emit("getDataEmit",racedata,room=activeusers["john@gmail.com"])
        
    

@socketio.on("connect")
def socketConnect():
    print("Connected ",request.sid)


@socketio.on("getData")
def getData():
    racedata={}
    standings = current.find_one({'Type':'standings'})
    print(standings)
    for n in range(0,len(standings)):
        a = current.find_one({'Type':'driver','Number':standings['Standings'][n]})
        if(a!=None):
            racedata['pos'+str(n+1)] = a["Info"]
    if(len(racedata)==len(standings)):
        racedata['number']=len(standings)
        emit("getDataEmit",racedata)


if __name__ == '__main__':
    socketio.run(app, debug=True)