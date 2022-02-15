#File to process images
import cv2
import numpy as np
import faceAnalysis as fa
import timeit as ti

def imageProcess(image, writeEmotion=True, writeRectangle=True, returnEmotion=False):
    #Objectives : detect faces, identify emotion associated on it, modify the image by framing faces and writing their emotions associated
    
    facesList = []
    emotionsList = []

    #Import faces and eyes detectors from cv2
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_eye.xml')

    #CV2 detection is made on gray pictures
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) #This return a list of tuple locating faces on image

    #For each face, detect eyes call imageProcess to process the face and modify the image
    for face in faces:
        x,y,w,h = face
        
        #Create blue rectangle around face of thickness 2
        if writeRectangle:
            cv2.rectangle(image, (x,y), (x+w,y+h), (255,0,0), 2 )
        
        #Select face image
        face_gray = gray[y:y+h, x:x+w]
        face_color = image[y:y+h, x:x+w]
        facesList.append(face_color)

        #Write emotion on the image
        if writeEmotion:
            emotion = fa.detectEmotion(face_color)
            cv2.putText(image, emotion, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            emotionsList.append(emotion)

    if returnEmotion: return emotionsList
    return facesList

def selectFace(image):
    #Return a face identified on an colored image

    #Import cv2 face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

    #Face detection is made on gray images
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.03, 5) #This return a list of tuple locating faces on image
    
    #The face returned is the first face detected on the image (if exists)
    if faces != []:
        x,y,w,h = faces[0]
        face = image[y:y+h, x:x+w]
        return face

#Some tests here.
# image = cv2.imread("cagnol.jpg", 1)  #Load Cagnol colored image
# imageProcess(image)
# cv2.imshow("Cagnol", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

