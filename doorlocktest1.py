import paho.mqtt.client as mqtt
import time
from firebase import firebase
import datetime
import time
import serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("/home/pi/Downloads/doorlock-63194-firebase-adminsdk-aasjv-b677970307.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
m_decode = ["unknown"]
i = 0
x = "a"

#FBConn = firebase.FirebaseApplication('https://doorlock-63194.firebaseio.com/', None)

def on_log(client, userdata, flags, buf):
    print("log: "+buf)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("bad connection returned code=",rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("disconnected result code "+str(rc))

def on_message(client,userdata,msg):
    topic = msg.topic
    global m_decode
    m_decode = msg.payload.decode()
    global i
    i = i+1
    print("message recieved",m_decode)
    for ids in m_decode :
      if msg.payload.decode() == ids :
       print("msg sends")
       client.publish("esp8266/DOOR",str(1))
       break
    else:
      client.publish("esp8266/DOOR",str(0))
      print(" ")
    
broker = "192.168.43.179"
client = mqtt.Client("python1")

client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_log = on_log
client.on_message = on_message

print("connecting to broker ", broker)
while True:
  client.connect(broker)
  client.loop_start()
  client.subscribe("esp8266/data")
  print(m_decode,i)
  while(m_decode[i] == x):
    continue
  doc_ref = db.collection('users').document( m_decode[i] )
  doc_ref.set({
    'first': input('name'),
    'last': input('class'),
    })
  users_ref = db.collection('users')
  docs = users_ref.stream()
  for doc in docs:
    print(doc.id, doc.to_dict()['first'])
  time.sleep(1)
  x = m_decode[i]
  client.loop_stop()
  client.disconnect()