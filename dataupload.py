from firebase import firebase
import paho.mqtt.client as mqtt
import time
import serial
import datetime

# Create the connection to our Firebase database - don't forget to change the URL!
FBConn = firebase.FirebaseApplication('https://doorlock-63194.firebaseio.com/', None)


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

broker = "192.168.0.9"
client = mqtt.Client("python1")

#client.on_connect = on_connect
#client.on_disconnect = on_disconnect
#client.on_log = on_log
#client.on_message = on_message
print("connecting to broker ", broker)
i=0
j=0
while True:
    
    #kid_1 = 0
    #kid_2 = 0
    #lasttime = 0
    from datetime import datetime
    # current date and time
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    print("timestamp =", timestamp)
    # Ask the user to input a temperature
    led1 = int(input("state of led1 "))

    # Create a dictionary to store the data before sending to the database
    data_led1 = {
        'state' : led1,
        'time' : timestamp
    }
    result_1 = FBConn.post('/led1',data_led1)

    led2 = int(input("state of led2 "))
    
    data_led2 = {
        'state' : led2,
        'time' : timestamp
    }
    # Post the data to the appropriate folder/branch within your database
       #state_1 = FBConn.get('/led1' ,None)
    result_2 = FBConn.post('/led2',data_led2)
    #result = FBConn.post('/strings', data={"xcv":"data"}, params={'print': 'pretty'})
    i = i+1
    j = j+1
    #state_2 = FBConn.get('/led2' ,None)

    #for k1 in state_1:
    #   if int(state_1[k1]['time']) > lasttime:
    #     lasttime = state_1[k1]['time']
    #     kid_1 = k1
    #lasttime = 0
    #for k2 in state_2:
    #   if int(state_2[k2]['time']) > lasttime:
    #     lasttime = state_2[k2]['time']
    #     kid_2 = k2 
    #print('last state of led1')
    #print(state_1[kid_1]['state'])
    
    #print('last state of led2')
    #print(state_2[kid_2]['state'])
    
    client.connect(broker)
    client.loop_start()
    #client.subscribe("esp8266/led1")
    #y = msg.payload
    #print(y)
    #client.publish("esp8266/led1",state_1[kid_1]['state'])
    time.sleep(0.5)
    client.loop_stop()
    client.disconnect()

    # Print the returned unique identifier
    #print(result_1)
#   print(value)

# Close the serial connection
ser.close()