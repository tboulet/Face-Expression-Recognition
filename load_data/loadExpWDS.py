import cv2
from utils import *
from config import input_shape
import imageProcess as ip
import numpy as np


def loadExpWData(nbrMaxImages=float('inf'), onlyDetected=False, detectedFace=False, count=False):
	folderImages = 'data/expW/images/'
	fileLabels = 'data/expW/labels.lst'

	file = open(fileLabels, 'r')
	nbrImages = 0
	k = 0
	X = []
	Y = []

	for line in file:
		if nbrImages>=nbrMaxImages: break
		k+= 1
		
		#Face extraction, according to the dataset annotations
		imageName, Id, top, left, right, bottom, cofidence, label = line.strip().split(' ')
		image = cv2.imread(folderImages+imageName)
		faceAccordingToDS = image[int(top):int(bottom), int(left):int(right)]     
		
		#Suivi visuel (facultatif, fait un peu peur sans attendre 1000ms entre deux images...)
		if False:
			cv2.imshow("ExpW importation...", faceAccordingToDS)
			if cv2.waitKey(1000) & 0xFF == ord('q'):
				break

		#Add extracted data to our dataset
	
		#Select detected face (if there is 1) or face according to the dataset
		if detectedFace:
			facesDetected = ip.imageProcess(faceAccordingToDS, writeEmotion=False, writeRectangle=False)
			if len(facesDetected) ==1:
				face = facesDetected[0]
			else:
				face = faceAccordingToDS
		else:
			face = faceAccordingToDS

		#Colored N*M*3 face to gray 48*48*1 image.
		gray = normAndResize(face, input_shape)	

		X.append(gray)
		Y.append(label)	#Emotion order is the same as fer2013.
		
		nbrImages += 1

		#Print number of datas loaded every 1000 datas

	X = np.array(X)
	Y = np.array(Y)
	print('\n')
	return X, Y







