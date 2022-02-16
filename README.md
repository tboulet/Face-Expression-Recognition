# Facial emotion detection and classification project

## Description :

Computer vision project aiming to detect and classify faces into 7 categories : Angry, Disgust, Fear, Happy, Sad, Surprise et Neutral.

The program use Cascade from CV2 to detect faces.
Faces are classified thanks to a CNN model inspired by VGG trained by myself.
I used several datasets for training my model.

## Python files to run :

You may need to install requirements using command ```pip install -r requirements.txt```


### run_videoCapture.py
Capture a video from your camera, detect faces and classify them.\

### run_game.py  
Start a game. You will have to mimic emotions displayed as fast as possible. You win 1 point for each emotion mimicked.\

Press "Q" to quit the game. Press "P" to pass the emotion (but you lose 1 point).\

Parameters of game(): 

    - playTime : duration of the game.
    - dt_required : duration required for maintaining emotion on screen to validate emotion.
    - n_photos : the program will temporaly save n_photos of you during the game, and then display them at the end.