import threading
from threading import Thread
from urllib.request import urlopen
import json
import pymongo
import time
import datetime
import certifi
from passlib.hash import pbkdf2_sha256
uri = "mongodb+srv://zahaanbatliboi:6rlwOJTWbstjuEDA@cluster0.jxt8hhc.mongodb.net/?retryWrites=true&w=majority"
cluster = pymongo.MongoClient(uri,tlsCAFile=certifi.where())
db = cluster["F1data"]
response = urlopen('https://api.openf1.org/v1/meetings?meeting_key=latest')
meeting=json.loads(response.read().decode('utf-8'))[0]
current = db[meeting["meeting_official_name"]]
import fastf1

drivernames={
    1:"VER",
    16:"LEC",
    4:"NOR",
    55:"SAI",
    11:"PER",
    81:"PIA",
    63:"RUS",
    44:"HAM",
    14:"ALO",
    22:"TSU",
    18:"STR",
    3:"RIC",
    38:"BEA",
    27:"HUL",
    10:"GAS",
    23:"ALB",
    31:"OCO",
    20:"MAG",
    24:"ZHO",
    77:"BOT",
    2:"SAR",
}
drivers=drivernames.keys()
print(drivers)
standingslist=[]

# Creating standings list which stores order of cars starting
for i in range(24):
    standingslist.append(0)
for i in drivers:
    response = urlopen('https://api.openf1.org/v1/position?session_key=latest&driver_number=' + str(i) + '&date>=' + str((datetime.datetime.now() - datetime.timedelta(seconds=5)).isoformat()))
    parsed=json.loads(response.read().decode('utf-8'))
    if(len(parsed)>0):
        position = parsed[-1]["position"]
        standingslist[position]=i
while(standingslist[-1]==0):
    standingslist.pop()
standingslist.pop(0)

standingsdb={
    'Type':'standings',
    'Standings':standingslist,
}
print(standingsdb)
current.insert_one(standingsdb)

def standings():
    global drivers
    global standingslist

    while True:
        standingslist=[]
        # Creating standings list which stores order of cars starting
        for i in range(24):
            standingslist.append(0)
        for i in drivers:
            response = urlopen('https://api.openf1.org/v1/position?session_key=latest&driver_number=' + str(i) + '&date>=' + str((datetime.datetime.now() - datetime.timedelta(seconds=5)).isoformat()))
            parsed=json.loads(response.read().decode('utf-8'))
            if(len(parsed)>0):
                position = parsed[-1]["position"]
                standingslist[position]=i
        while(standingslist[-1]==0):
            standingslist.pop()
        standingslist.pop(0)

        current.update_one({'Type':'standings'}, {"$set":{"Standings":standingslist}})


def info(driver):
    global drivernames
    main={
        'Number':driver,
        'Name':drivernames[driver],
        'DRS':0,
        'Speed':0,
        'Last':0,
        'S1':0,
        'S2':0,
        'S3':0,
        'Compound':0,
        'Age':0,
        'Leader':0,
        'Ahead':0,
        'Gaining':0,
    }
    initial={
        'Type':'driver',
        'Number':driver,
        'Info':main,
    }
    current.insert_one(initial)
    while True:
        response = urlopen('https://api.openf1.org/v1/car_data?session_key=latest&driver_number=' + str(driver) + '&date>=' + str((datetime.datetime.now() - datetime.timedelta(seconds=5)).isoformat()))
        car=json.loads(response.read().decode('utf-8'))[-1]
        response = urlopen('https://api.openf1.org/v1/laps?session_key=latest&driver_number=' + str(driver) + '&date>=' + str((datetime.datetime.now() - datetime.timedelta(minutes=7)).isoformat()))
        lastlaps=json.loads(response.read().decode('utf-8'))
        response = urlopen('https://api.openf1.org/v1/intervals?session_key=latest&driver_number=' + str(driver) + '&date>=' + str((datetime.datetime.now() - datetime.timedelta(seconds=5)).isoformat()))
        interval=json.loads(response.read().decode('utf-8'))[-1]

        if(car['drs']>=10):
            main['DRS']=2
        elif(car['drs']==8):
            main['DRS']=1
        else:
            main['DRS']=0
        
        main['Speed']=car['speed']

        if(len(lastlaps)>1):
            if(lastlaps[-1]['is_pit_out_lap']==True):
                main['Last']=0
            else:
                lastlap=lastlaps[-1]
                main['Last']=lastlap['lap_duration']
                main['S1']=lastlap['duration_sector_1']
                main['S2']=lastlap['duration_sector_2']
                main['S3']=lastlap['duration_sector_3']
        else:
           main['Last']=0 

        main['Leader']=interval['gap_to_leader']
        main['Ahead']=interval['interval']

        if(standingslist.index(driver)>0 and lastlap['lap_number']>0):
            carahead=current.find_one({'Number':standingslist[standingslist.index(driver)-1]})
        main['Gaining']=carahead['Last']-main['Last']

        current.update_one({'Type':'driver','Number':driver}, {"$set":{"Info":main}})

standingsthread=threading.Thread(target=standings)
threads=[]
for i in drivers:
    thread = threading.Thread(target=info, args=(i,))
    threads.append(thread)

standingsthread.start()
for i in threads:
    i.start()
    
standingsthread.join()
for i in threads:
    i.join()
