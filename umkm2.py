import sys
import Adafruit_DHT
import urllib.request
import urllib.parse
import json
import ast
import struct
import base64
import os
import time
import threading
import math
import subprocess
import logging
from datetime import datetime as dt
import picamera
import smbus
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

bus = smbus.SMBus(1)

url_suhu = "https://gh1.rumahkuhidroponik.com/post_suhu.php"
url_image = "https://gh1.rumahkuhidroponik.com/post_image.php"
url_realtime = "https://rumahkuhidroponik.com/API/sensor/update-device3/"
url_baru = "https://smartghsip.belajarobot.com/sensor/insert/1"
#url_lux =  "https://rumahkuhidroponik.com/API/sensor/update-device1/"
url_lux = "https://gh1.rumahkuhidroponik.com/post_ppm.php"
api_key = "a1ffqsVcx45IuG"

sensor = Adafruit_DHT.DHT22
pin = 4
hum = 0
temp = 0
lux = 0
camera = picamera.PiCamera()
hostname = "8.8.8.8"
datenow = dt.now().strftime("%Y-%m-%d")

# setup logging
logging.basicConfig(filename='logs/project_' + datenow + '.log', filemode='w',
        format='%(levelname)s | %(asctime)s | %(message)s', level=logging.DEBUG)

def cam():
   camera.resolution = (320, 240)
   camera.rotation = 180
   camera.start_preview()
   time.sleep(1)
   camera.capture('example.jpg')
   camera.stop_preview()

   with open("example.jpg", "rb") as img_file:
        Image = base64.b64encode(img_file.read())

   headers = {}
   headers['Content-Type'] = 'application/json'

   files = urllib.parse.urlencode({
       'api_key':api_key,
       'image':Image
        }).encode('ascii')
   try:
      send_image = urllib.request.urlopen(url_image, data = files)
      print(send_image.read())
   except:
      print("post image bermasalah!")

def realtime():
   camera.resolution = (320, 240)
   camera.rotation = 180
   camera.start_preview()
   time.sleep(0.5)
   camera.capture('example.jpg')
   camera.stop_preview()
   humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
   readLux()
   luxvalue = int(lux)
   temp = int(temperature)
   hum = int(humidity)
   with open("example.jpg", "rb") as img_file:
        Image = base64.b64encode(img_file.read())

   headers = {}
   #headers['Content-Type'] = 'application/json'
   headers['Content-Type'] = 'application/x-www-form-urlencoded'
   files = urllib.parse.urlencode({
       #'api':api_key,
       #'id':'0001',
       'ppm':luxvalue,
       'temp':temp,
       'humid':hum,
       'image':Image
        }).encode('ascii')
   try:
      send_image = urllib.request.urlopen(url_baru, data = files)
      print(send_image.read())
   except:
      print("post image bermasalah!")

def dht22():
   humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
   temp = round(temperature)
   hum = round(humidity)

   headers = {}
   headers ['Content-Type'] = 'application/json'

   data = urllib.parse.urlencode({
       'api_key':api_key,
       'Suhu':temp,
       'Kelembapan':hum
        }).encode('ascii')
   try:
      send = urllib.request.urlopen(url_suhu, data = data)
      print(send.read())
   except:
      print("post suhu bermasalah")

def postLux():
   readLux()
   luxvalue = round(lux)

   headers = {}
   headers ['Content-Type'] = 'application/json'   
   data = urllib.parse.urlencode({
       'api_key':api_key,
       'PPm':luxvalue
        }).encode('ascii')
   try:
      send = urllib.request.urlopen(url_lux, data = data)
      print(send.read())
   except:
      print("post Lux bermasalah")


def readLux():
   try:
      global lux
      bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
      bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
      time.sleep(0.5)
      dataL = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
      lux = dataL[1] *256 + dataL[0]
      print ("lux = %d: " %lux)
   except:
      print ("data sensor lux bermasalah")

menit = 0
jam = 0
flag = 0
flag1 = 0

#def maincode():
#    global menit
#    if menit != dt.now().minute:
#       cam()
#       dht22()
#       menit = dt.now().minute

def maincode():
    global flag
    if dt.now().hour == 10 and dt.now().minute == 0 and flag == 0:
       print(dt.now().hour, dt.now().minute)
       cam()
       dht22()
       postLux()
       flag = 1
    if dt.now().hour == 14 and dt.now().minute == 0 and flag == 0:
       print(dt.now().hour, dt.now().minute)
       cam()
       dht22()
       postLux()
       flag = 1

    if dt.now().hour == 15 and dt.now().minute == 0:
       flag = 0
       print(flag)

#    if dt.now().hour == 0 and dt.now().minute == 0 and dt.now().second == 0:
#       sudo reboot

def mainloop():
    #readLux()
    global menit
    global flag1
    if menit != dt.now().minute:
       #readLux()
       flag1 += 1
       if flag1 == 5:
          realtime()
       if flag1 > 5:
          flag1 = 0
       menit = dt.now().minute

while True:
   response = os.system("ping -c3 " + hostname)
   if response == 0:
      maincode()
      mainloop()
   if response != 0:
      print("Device not connected to Internet")
