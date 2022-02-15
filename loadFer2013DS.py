# This file load the dataset fer2013 as arrays.
import csv
import numpy as np
import cv2
import matplotlib.pyplot as plt
from config import input_shape
from utils import *


def strToArray(string):  # Fer2013 provides images as string so it needs to be transformed
    A = []
    lenght = len(string)
    i = 0
    nbr = ""

    while i < lenght:
        car = string[i]

        if car != " ":
            nbr += car
        else:
            A.append(int(nbr))
            nbr = ""
        i += 1
    A.append(int(nbr))

    A = np.array(A)
    A = np.reshape(A, (48,48,1))

    return A


# LOAD DATA AS ARRAY

def loadFer2013Data(maxNbrImages=35887):
    print(f"\nCHARGEMENT DE {maxNbrImages} DONNEES DEPUIS FER2013 ...")

    maxNbrImages = min(maxNbrImages, 35887)
    filename = "data/fer2013/fer2013.csv"
    emotions = ["Angry", "Disgust", "Fear",
                "Happy", "Sad", "Suprise", "Neutral"]

    X = []
    Y = []

    with open(filename, 'r', encoding='utf-8') as file:

        csv_reader = csv.reader(file, delimiter=",")
        next(csv_reader)  # Passe la ligne de titre

        i = 0
        for row in csv_reader:
            i += 1
            if i > maxNbrImages:
                break

            emotionNbr, stringImage, typeImage = row

            X.append(normAndResize(strToArray(stringImage), input_shape))
            Y.append(emotionNbr)

            print(f"Donnée {i} sur {maxNbrImages} chargée", end='\r')

    X = np.array(X)
    Y = np.array(Y)
    print(f"{maxNbrImages} données chargées depuis fer2013.")
    return X, Y
