import os
import cv2
from utils import *
import imageProcess as ip
from config import input_shape


def extractDataFromVideo_(filename, videoName, facesList, labelsList, maxNbrImages, frameRate):
    # Extract every faces in a specified video and add it to a list of faces as well as labels corresponding.
    emotions = ["Neutral", "Angry", "Disgust",
                "Fear", "Happy", "Sad", "Suprise"]

    # Start capture of a video and reading of a label file. Dont change the lists if file can not be read.
    cap = cv2.VideoCapture(filename)
    if (cap.isOpened() == False):
        print("Error opening video")

    try:
        file = open("data/affwild/labels/"+videoName[:-4]+'.txt', 'r')
    except FileNotFoundError:
        return facesList, labelsList
    file.readline()

    # Read until video is completed
    k = 0
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        line = file.readline()

        if ret == True:
            k += 1

            if k*frameRate >= 1:  # Read a frame each N frames where N=1/frameRate
                k = 0

                # Load image and labels

                # Detect faces on the image
                newFaces = ip.imageProcess(frame, writeEmotion=False)

                # If 2 faces were detected, it means an error was made since there is only single-person videos here.
                # The second condition means the image is irrelevant (no face on the picture)
                if len(newFaces) == 1 and line[0] != '-':
                    facesList += newFaces

                    emotionNbr = emotionToNumber(emotions[int(line[0])])
                    labelsList.append(emotionNbr)
                elif False:
                    print(
                        "Erreur pour la donnée : Aucun ou plusieurs visages détectés", end='\r')

                # If we overreach the maximum number of images desired, stop
                if len(facesList) > maxNbrImages:
                    break

            # Press Q on keyboard to  exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Display the resulting frame
            if False:
                cv2.imshow('AffWild data extraction...', frame)

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    # Close file
    file.close()

    # Return face and label lists with new datas
    return facesList, labelsList





# LOAD DATA

def loadAffwildData(maxNbrImages=10000000000, frameRate=1/20):
    print(f"\nCHARGEMENT DE {maxNbrImages} DONNEES DEPUIS AFFWILD...")

    foldername = "data/affwild/videos/"
    facesList = []
    labelsList = []
    maxNbrImages -= 1
    k = 0
    nbrOfVideos = len(os.listdir(foldername))

    # For each video...
    for videoName in os.listdir(foldername):

        # If we overreach the maximum number of images desired, stop
        if len(facesList) >= maxNbrImages:
            break

        elif videoName+'_left' in os.listdir("data/affwild/labels") or videoName+'_right' in os.listdir("data/affwild/labels"):
            print("Vidéo à deux visages, non pris en compte")

        else:
            k += 1
            print(f"Traitement de {videoName}, video {k}/{nbrOfVideos}")
            filename = foldername+videoName

            # Press Q on keyboard to exit ONE video
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Add datas extracted from the specified video to features and labels
            facesList, labelsList = extractDataFromVideo_(
                filename, videoName, facesList, labelsList, maxNbrImages, frameRate)

    # List of colored images N*M*3 faces to array of gray images 48*48*1
    N = len(facesList)
    print(
        f"TRAITEMENT AFFWILD: traitement des {N} visages détectés sur les vidéos de AffWild...")

    for k in range(N):
        visage = facesList[k]
        facesList[k] = normAndResize(visage, input_shape)
    X = np.array(facesList)

    Y = np.array(labelsList)

    print(N, "données chargées depuis AffWild.")
    return X, Y