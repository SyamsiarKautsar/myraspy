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

#url_suhu = "https://gh1.rumahkuhidroponik.com/post_suhu.php"
#url_image = "https://gh1.rumahkuhidroponik.com/post_image.php"
#url_realtime = "https://rumahkuhidroponik.com/API/sensor/update-device3/"
url_baru = "https://smartghsip.belajarobot.com/sensor/insert/1"
#url_lux =  "https://rumahkuhidroponik.com/API/sensor/update-device1/"
#url_lux = "https://gh1.rumahkuhidroponik.com/post_ppm.php"
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
#logging.basicConfig(filename='logs/project_' + datenow + '.log', filemode='w',
#        format='%(levelname)s | %(asctime)s | %(message)s', level=logging.DEBUG)


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
       'lumen':luxvalue,
       'temp':temp,
       'humid':hum,
       'image':Image
        }).encode('ascii')
   try:
      send_image = urllib.request.urlopen(url_baru, data = files)
      print(send_image.read())
   except:
      print("post image bermasalah!")



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


def mainloop():
    #readLux()
    global menit
    global flag1
    if menit != dt.now().minute:
       #readLux()
       flag1 += 1
       if flag1 == 2:
          realtime()
       if flag1 > 2:
          flag1 = 0
       menit = dt.now().minute

while True:
   response = os.system("ping -c3 " + hostname)
   if response == 0:
      #maincode()
      mainloop()
   if response != 0:
      print("Device not connected to Internet")
