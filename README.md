# Facial emotion detection and classification project

## Description :

Computer vision project aiming to detect and classify faces into 7 categories : Angry, Disgust, Fear, Happy, Sad, Surprise et Neutral.

The program use Cascade from CV2 to detect faces.
Faces are classified thanks to a CNN model inspired by VGG trained by myself.

I used several datasets for training my model : 

    - Aff-Wild
    - ExpW (Expression in-the-Wild)
    - FER-2013
    - Ravdess (faces are extracted from videos)

## Python files to run :

You may need to install requirements using command ```pip install -r requirements.txt```


### run_videoCapture.py
Capture a video from your camera, detect faces and classify them.

    python run_videoCapture.py

### run_game.py  
Start a game. You will have to mimic emotions displayed as fast as possible. You win 1 point for each emotion mimicked.

    python run_game.py -p time_play -m time_maintain -s nbr_screen

Press "Q" to quit the game. Press "P" to pass the emotion (but you lose 1 point).

Options of game(): 

    - p : duration of the game.
    - m : duration required for maintaining emotion on screen to validate emotion.
    - s : the program will temporaly save s of you during the game, and then display them at the end.
