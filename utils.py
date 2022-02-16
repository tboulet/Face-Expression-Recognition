import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf


def afficher(image):
    if len(image.shape) == 3:
        if image.shape[2] == 3:  # (h,l,3)
            plt.imshow(image)
        elif image.shape[2] == 1:  # (h,l,1)->(h,l)
            image2 = image
            plt.imshow(tf.squeeze(image))
    elif len(image.shape) == 2:  # (h,l)
        plt.imshow(image)


def predir(modele, image):
    # Return output of image from modele
    return modele(np.array([image]))[0, :]

def normAndResize(image, input_shape):
    # For an array image of shape (a,b,c) or (a,b), transform it into (h,l,p). Also normalize it.

    h, l, p = input_shape
    # resize for h and l     
    image = cv2.resize(image, dsize=(h, l), interpolation=cv2.INTER_CUBIC)
    # if we want (h,l,3) -> (h,l,1) , we first transform it in to (h,l) (grey the image)
    if len(image.shape) == 3 and p == 1 and image.shape[2] != 1:
        image = image.mean(2)
    image = np.reshape(image, (h, l, p))  # restore third dimension
    image = image.astype("float32")
    image = (image/127.5)-1  # normalisation

    return image


def emotionToNumber(emotion):
    emotions = ["Angry", "Disgust", "Fear",
                "Happy", "Sad", "Suprise", "Neutral"]
    return emotions.index(emotion)

def stackImages(listOfArrayImage):
    liste = []
    for X in listOfArrayImage:
        liste += X.tolist()
    return np.stack(liste, axis=0)
    

def mergeToDatabase(listOfX, listOfY, validation_repart=[0.1, 0.1, 0.1, 0.1]):
    # This shuffle each X, extract validation data, merge differents X, shuffle again.
    listOfX_train, listOfY_train = [], []
    listOfX_test, listOfY_test = [], []

    for X, Y, rate in zip(listOfX, listOfY, validation_repart):
        N = X.shape[0]

        # Shuffle each X and Y the same way
        shuffler = np.random.permutation(N)
        X, Y = X[shuffler], Y[shuffler]
        # Extract validation data
        X_train, Y_train = X[:int(N*(1-rate))], Y[:int(N*(1-rate))]
        X_test, Y_test = X[int(N*(1-rate)):], Y[int(N*(1-rate)):]
        listOfX_train.append(X_train)
        listOfY_train.append(Y_train)
        listOfX_test.append(X_test)
        listOfY_test.append(Y_test)
    # Merge
    BigX_train = stackImages(listOfX_train)
    BigY_train = stackImages(listOfY_train)

    BigX_test = stackImages(listOfX_test)
    BigY_test = stackImages(listOfY_test)
    # Shuffle the whole
    shuffler = np.random.permutation(len(BigX_train))
    BigX_train = BigX_train[shuffler]
    BigY_train = BigY_train[shuffler]

    shuffler = np.random.permutation(len(BigX_test))
    BigX_test = BigX_test[shuffler]
    BigY_test = BigY_test[shuffler]

    return BigX_train, BigY_train, BigX_test, BigY_test
