import time
import pyrebase
import random

#from pyjoystick.sdl2 import Key, Joystick, run_event_loop


#config = {
#  "apiKey": "apiKey",
#  "authDomain": "mobilerobotgh-eb60a.firebaseapp.com",
#  "databaseURL": "https://databaseName.firebaseio.com",
#  "storageBucket": "mobilerobotgh-eb60a.appspot.com"
#}

config = {
  "apiKey": "AIzaSyAUK_-9jzfpKwkj1yPlUvnIzNrjwmT13Sc",
  "authDomain": "trymobilerobot.firebaseapp.com",
  "databaseURL": "https://trymobilerobot-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "trymobilerobot.appspot.com"
}

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
#auth = firebase.auth()

# Log the user in
#user = auth.sign_in_with_email_and_password('cs.belajarobot@gmail.com', '12345abcde')

# Get a reference to the database service
#"nilai"
while True:                                                                              #the beginning of the main program.
    database = firebase.database()                                             #take an instance from the firebase database which is pointing to the root directory of your database.
    #dbread = database.child("Console")                            #get the child "RGBControl" path in your database and store it inside the "RGBControlBucket" variable.
    #nilai= dbread.child("Kanan").get().val()                        #read the power state value from the tag "powerState" which is a node inside the database.
    angka = random.randint(1,100)
    database.child("Console").child("Arah").update({"Arah": angka})
    database.child("Console").child("Servo").update({"Servo": angka})
    print(angka)
    #run_event_loop(print_add, print_remove, key_received)
    time.sleep(1)

