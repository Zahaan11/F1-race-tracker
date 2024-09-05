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
response = urlopen('https://api.openf1.org/v1/session?session_key=latest')
latest=json.loads(response.read().decode('utf-8'))[0]
current = db[latest["session_key"]]
import fastf1

data=[]
for n in range(1,current+1):
    response = urlopen('https://api.openf1.org/v1/session?session_key=' + str(n))
    overall=json.loads(response.read().decode('utf-8'))[0]
    response = urlopen('https://api.openf1.org/v1/stints?session_key=' + str(n))
    stints=json.loads(response.read().decode('utf-8')) 



# Import pandas library
import pandas as pd

# initialize list of lists
data = [['tom', 10], ['nick', 15], ['juli', 14]]

# Create the pandas DataFrame
df = pd.DataFrame(data, columns=['Name', 'Age'])

# print dataframe.
print(df)
