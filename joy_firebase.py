import sys
import time
import pygame
import pyrebase
import random

from pygame.locals import *
pygame.init()

pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())

flaga = 0
flagb = 0

config = {
  "apiKey": "AIzaSyAUK_-9jzfpKwkj1yPlUvnIzNrjwmT13Sc",
  "authDomain": "trymobilerobot.firebaseapp.com",
  "databaseURL": "https://trymobilerobot-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "trymobilerobot.appspot.com"
}

firebase = pyrebase.initialize_app(config)

database = firebase.database()


while True:
    
    for event in pygame.event.get():
        database = firebase.database()
        if event.type == JOYBUTTONDOWN:
            #print(event.button)
            if event.button == 0:
                print("servo reset")
                database.child("Console").update({"Servo": 8})
            
        if event.type == JOYHATMOTION:
            if event.value[0] == -1:
                print("kiri")
                database.child("Console").update({"Arah": 3})
            elif event.value[0] == 1:
                print("kanan")
                database.child("Console").update({"Arah": 4})
            elif event.value[1] == -1:
                print("mundur")
                database.child("Console").update({"Arah": 2})
            elif event.value[1] == 1:
                print("maju")
                database.child("Console").update({"Arah": 1})
            else:
                print("stop")
                database.child("Console").update({"Arah": 0})
        if event.type == JOYAXISMOTION:
            if event.axis == 3:
                #motion[event.axis] = event.value
                if event.value <-0.9 and flaga == 0:
                   print("servo_up")
                   database.child("Console").update({"Servo": 1})
                   flaga = 1
                elif event.value>0.9 and flaga == 0:
                   print("servo down")
                   database.child("Console").update({"Servo": 2})
                   flaga = 1
                elif event.value>-0.1 or event.value<0.1:
                   if flaga == 1:
                      print("stop servo updown")
                      database.child("Console").update({"Servo": 0})
                      flaga = 0

            if event.axis == 2:
                #motion[event.axis] = event.value
                if event.value <-0.9 and flagb == 0:
                   print("servo_left")
                   database.child("Console").update({"Servo": 3})
                   flagb = 1
                elif event.value>0.9 and flagb == 0:
                   print("servo right")
                   database.child("Console").update({"Servo": 4})
                   flagb = 1
                elif event.value>-0.1 or event.value<0.1:
                   if flagb == 1:
                      print("stop servo rightleft")
                      database.child("Console").update({"Servo": 0})
                      flagb = 0
    time.sleep(0.25)