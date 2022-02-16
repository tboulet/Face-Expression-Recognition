import os
import cv2
from utils import *
import imageProcess as ip
from config import input_shape


def extractDataFromVideo(filename, videoName, facesList, labelsList, maxNbrImages, frameRate):
    # Extract every faces in a specified video and add it to a list of faces as well as labels corresponding.

    # Start capture of a video
    cap = cv2.VideoCapture(filename)
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    emotions_ravdess = ["_", "Neutral", "Calm", "Happy",
                "Sad", "Angry", "Fear", "Disgust", "Suprise"]

    # Read until video is completed
    k = 0
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            k += 1
            

            if k*frameRate >= 1:  # Read a frame each N frames where N=1/frameRate
                k = 0

                # Load image and labels

                # Ravdess emotions list is not in the same order as fer2013 (reference)
                emotionNbr = int(videoName[7])
                emotion = emotions_ravdess[emotionNbr]
                emotionNbr = emotionToNumber(emotion)

                # Detect faces on the image
                newFaces = ip.imageProcess(frame, writeEmotion=False)

                # If 2 faces were detected, it means an error was made since there is only single-person videos.
                if len(newFaces) == 1:
                    facesList += newFaces
                    labelsList.append(emotionNbr)

                # If we overreach the maximum number of images desired, stop
                if len(facesList) >= maxNbrImages:
                    break

            # Display the resulting frame
            if False:
                cv2.imshow('Frame', frame)

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    # Return face and label lists with new datas
    return facesList, labelsList


# LOAD DATA

def loadRavdessData(maxNbrImages=10000000000, frameRate = 1/20):

    foldername = "data/ravdess/videos/"
    
    facesList = []
    labelsList = []

    # For each actor...
    for actorName in os.listdir(foldername):

        # If we overreach the maximum number of images desired, stop
        if len(facesList) >= maxNbrImages:
            break
        
        videoNames = os.listdir(foldername+actorName)
        nbrOfVideos = len(videoNames)

        k = 0
        # For each video...
        for videoName in videoNames:

            # If we overreach the maximum number of images desired, stop
            if len(facesList) >= maxNbrImages:
                break

            k += 1
            filename = foldername+actorName+'/'+videoName

            if videoName[7] == '2':
                pass

            elif videoName[7] in [str(n) for n in range(1, 9)]:
                # Add datas extracted from the specified video to features and labels
                facesList, labelsList = extractDataFromVideo(
                    filename, videoName, facesList, labelsList, maxNbrImages, frameRate)

    # List of colored images N*M*3 faces to array of gray images 48*48*1
    N = len(facesList)

    for k in range(N):
        visage = facesList[k]
        facesList[k] = normAndResize(visage, input_shape)
    X = np.array(facesList)

    Y = np.array(labelsList)

    return X, Y