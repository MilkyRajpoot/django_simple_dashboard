from pymongo import MongoClient
import pymongo
import datetime
import urllib.parse
import RPi.GPIO as GPIO
import time
import picamera
import gridfs
PIR_input = 29
LED = 32
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_input,GPIO.IN)
GPIO.setup(LED,GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

client = MongoClient("mongodb://iot:"+urllib.parse.quote('@')+'maapapa19'+"@cluster0-shard-00-00-bfyv0.mongodb.net:27017,cluster0-shard-00-01-bfyv0.mongodb.net:27017,cluster0-shard-00-02-bfyv0.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db=client.smart;
print(db)
data=db.door

while True:
    if(GPIO.input(PIR_input)):
        GPIO.output(LED, GPIO.HIGH)
        msg = "Motion Detected"
        datet = datetime.datetime.now()
        camera=picamera.PiCamera()
        img = camera.capture('example.jpg')
        result = data.insert_one({ "date":datet,"pirdata":msg,"image":img,"allow":False})
        print(result)
        time.sleep(60)
        time.sleep(60) 
    else: 
        GPIO.output(LED, GPIO.LOW)

 
