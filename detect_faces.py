import numpy as np 
import argparse
import cv2

# construct and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m". "--model", required=True, help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

#load model using prototxt and model file paths
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

#load input image
image = cv2.imread(args["image"])
#extract dimensions
(h, w) = image.shape[:2]
#create blob and resize to 300x300
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

#detect faces
print("[INFO] computing object detections...")
net.setInput(blob)
detections = net.forward()

#loop over the detections
for i in range(0, detections.shape[2]):
	#extract probability associated with prediction
	confidence = detections[0, 0, i ,2]

	#filter out weak detections by comparing confidence and min confidence
	if confidence > args["confidence"]:
		#compute coordinates of box 
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")

		#draw box with associated probability
		text = "{:.2f}%".format(confidence * 100)
		y = startY - 10 if startY - 10 > 10 else startY + 10
		cv2.rectange(image, (startX, startY), (endX, endY), (0, 0 , 255), 2)
		cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

#print image
cv2.imshow("Output", image)
cv2.waitKey(0)
