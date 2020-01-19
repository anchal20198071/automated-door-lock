from firebase import firebase
import datetime
import time
import serial

# Create the connection to our Firebase database - don't forget to change the URL!
FBConn = firebase.FirebaseApplication('https://doorlock-63194.firebaseio.com/', None)

i=0
while True:
    
    kid_1 = 0
    kid_2 = 0
    lasttime = 0
    from datetime import datetime
    # current date and time
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    print("timestamp =", timestamp)
    # Ask the user to input a temperature
    led1 = int(input("state of led1 "))
    led2 = int(input("state of led2 "))
    
    # Create a dictionary to store the data before sending to the database
    data_led1 = {
        'state' : led1,
        'time' : timestamp
    }
    data_led2 = {
        'state' : led2,
        'time' : timestamp
    }
    # Post the data to the appropriate folder/branch within your database
    result_1 = FBConn.post('/led1',data_led1)
    state_1 = FBConn.get('/led1' ,None)
    result_2 = FBConn.post('/led2',data_led2)
    state_2 = FBConn.get('/led2' ,None)

    for k1 in state_1:
       if int(state_1[k1]['time']) > lasttime:
         lasttime = state_1[k1]['time']
         kid_1 = k1
    lasttime = 0
    for k2 in state_2:
       if int(state_2[k2]['time']) > lasttime:
         lasttime = state_2[k2]['time']
         kid_2 = k2 
    print('last state of led1')
    print(state_1[kid_1]['state'])
    print('last state of led2')
    print(state_2[kid_2]['state'])
    i = i + 1

    # Print the returned unique identifier
    print(result_1)
#   print(value)

# Close the serial connection
ser.close()