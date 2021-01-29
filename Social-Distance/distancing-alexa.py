import numpy as np
import time
import cv2
import math
import os
import boto3
from boto.s3.key import Key

def upload_to_s3(i,text):

	from botocore.client import Config


    ACCESS_KEY_ID = """ Enter AWS Access Key ID"""
	ACCESS_SECRET_KEY = """ Enter AWS Secret Access Key"""
	BUCKET_NAME = """ Enter AWS Access S3 Bucket Name"""
	BUCKET_NAME1 = """ Enter AWS Access S3 Bucket Name"""


	data = open('SDimage.png', 'rb')
	f = open('SDstatus.txt', 'w')
    
	s3 = boto3.resource(
    	's3',
    	aws_access_key_id=ACCESS_KEY_ID,
    	aws_secret_access_key=ACCESS_SECRET_KEY,
    	config=Config(signature_version='s3v4')
	)
	s3.Bucket(BUCKET_NAME).put_object(Key='SDimage.png', Body=data)
	f.write(text)
	f.close()
	f=open("SDstatus.txt",'r+')
	s3.Bucket(BUCKET_NAME1).put_object(Key='SDstatus.txt', Body=f.read())
	print ("Done")

labelsPath = "./coco.names"
LABELS = open(labelsPath).read().strip().split("\n")

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

weightsPath = "./yolov3.weights"
configPath = "./yolov3.cfg"

net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)


cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    
    ret,image=cap.read()
    (H, W) = image.shape[:2]
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()
    print("Frame Prediction Time : {:.6f} seconds".format(end - start))
    boxes = []
    confidences = []
    classIDs = []
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > 0.1 and classID == 0:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
                
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5,0.3)
    ind = []
    for i in range(0,len(classIDs)):
        if(classIDs[i]==0):
            ind.append(i)
    a = []
    b = []

    if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                a.append(x)
                b.append(y)
                
    distance=[] 
    nsd = []
    for i in range(0,len(a)-1):
        for k in range(1,len(a)):
            if(k==i):
                break
            else:
                x_dist = (a[k] - a[i])
                y_dist = (b[k] - b[i])
                d = math.sqrt(x_dist * x_dist + y_dist * y_dist)
                distance.append(d)
                if(d <=250):
                    nsd.append(i)
                    nsd.append(k)
                nsd = list(dict.fromkeys(nsd))
                print(nsd)
    color1 = (0, 0, 255) 
    color = (0, 255, 0)
    text=""
    p=0
     
    if len(idxs) > 0:
        for i in idxs.flatten():
            if (i in nsd):
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                cv2.rectangle(image, (x, y), (x + w, y + h), color1, 2)
                text = "Alert"
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color1, 2)
            else:
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = 'OK'
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)   
            p=p+1
    
    cv2.imshow("Social Distancing Detector", image)
    cv2.imwrite('SDimage.png',image)
    print(text)
    upload_to_s3(p,text)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
