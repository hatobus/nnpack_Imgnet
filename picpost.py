import paho.mqtt.client as mqtt
from PIL import Image
import json
import random
from io import BytesIO
import os, re, glob
import time
import base64
import cv2


# videocaptureが開かれない時は以下のコメントで有効化する
# sudo modprobe bcm2835-v4l2

host = "192.168.179.7"
port = 1883
topic = "/pub/gun/image"

client = mqtt.Client(protocol=mqtt.MQTTv311)

client.connect(host, port=port, keepalive=30)

WIDTH, HEIGHT = 416, 416

def ToB64(fname):
    with open(fname, "rb") as f:
        img_base64 = base64.b64encode(f.read())

    return img_base64

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))
a=0
while True:
    cap = cv2.VideoCapture(0)
    retval, image = cap.read()
    retval, buf = cv2.imencode(".jpg", image)
    jpg2txt = base64.b64encode(buf)
    print(jpg2txt)
    cv2.imwrite("./tmp/output"+str(a)+".jpg", image)
    a+=1
    cap.release()
    client.publish(topic, payload=jpg2txt)
    time.sleep(1)
    print("put")

cv2.destroyAllWindows()

client.disconnect()

