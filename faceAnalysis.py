#Objective of this file is to analyse a face
print("Load model...")
import numpy as np
from utils import *
from config import emotions, input_shape, modelName

model = tf.keras.models.load_model("models/"+modelName)	#Load our model

print('Model used:', modelName)

def detectEmotion(face):
	#Return the most likely emotion there is on a face
	
	face = normAndResize(face, input_shape)		#Process our image for input of model

	emotionVect = predir(model, face)
	emotionNbr = np.argmax(emotionVect)			 
	emotion = emotions[emotionNbr]
	return emotion
