import paho.mqtt.client as mqtt
import time
from firebase import firebase
import datetime
import time
import serial

#FBConn = firebase.FirebaseApplication('https://doorlock-63194.firebaseio.com/', None)

i=0

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
    m_decode = str(msg.payload.decode("utf-8","ignore"))
    print("message recieved",m_decode)
broker = "192.168.43.179"
client = mqtt.Client("python1")

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_log = on_log
client.on_message = on_message

print("connecting to broker ", broker)
i=0
while True:
  m = input("enter 0 or 1")
  client.connect(broker)
  client.loop_start()
  client.subscribe("esp8266/data")
  #y = msg.payload
  #print(y)
  client.publish("esp8266/DOOR", m)
  time.sleep(1)
  client.loop_stop()
  client.disconnect()
  i = i+1