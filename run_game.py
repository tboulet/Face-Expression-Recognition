import argparse


def smileyRandom(emotionToDodge):
    #Return a random smiley and the emotion associated

    import cv2
    import random
    from config import emotions

    emotionNbr = random.randrange(0,6)
    emotion = emotions[emotionNbr]
    if emotion == emotionToDodge: return smileyRandom(emotion)
    smileyImagePath = "smileys/"+emotion+".png"
    smiley = cv2.imread(smileyImagePath)
    return smiley, emotion


def game(time_play = 30, time_maintain=0.5, screen=0, invincibleFrame=0.5):
    '''Play a game.
    time_play : duration of the game.
    time_maintain : duration required for maintaining emotion on screen to validate emotion.
    screen : number of screen the program will temporaly save of you during the game, and then display them at the end.
    invincibleFrame : time during you can't score any point if you already scored one before.
    '''

    #Use your camera for processing the video. Stop by pressing Q
    import cv2
    import matplotlib.pyplot as plt
    import imageProcess as ip
    import time


    cap = cv2.VideoCapture(0)   #0 means we capture the first camera, your webcam probably
    cv2.namedWindow("Camera",cv2.WINDOW_NORMAL)
    score = 0       

    timeScoring = time.time()   #last instant an emotion was found.
    timeInitial = time.time()
    timeSinceOtherEmotions = time.time()
    timeLastPhoto = time.time()

    smiley, emotion = smileyRandom("")
    smileyNeutral = smiley.copy()
    photos= []





    while cap.isOpened():		
        ret, frame = cap.read()  #Read next video frame, stop if frame not well read
        if not ret: break
        
        emotionsList = ip.imageProcess(frame, returnEmotion=True)
        
        
        if time.time()-timeSinceOtherEmotions > time_maintain:    #If emotions maintained for dt seconds, score is increased and a new smiley is generated
            score += 1
            smiley, emotion = smileyRandom(emotion)
            smileyNeutral = smiley.copy()
            timeScoring = time.time()
            timeSinceOtherEmotions = time.time()
        
        elif emotion in emotionsList and time.time()-timeScoring>invincibleFrame: #If emotion recognized, increase score, reset smiley to mimick, start timer for impossibility of scoring (0.5s)
            pass

        else:
            timeSinceOtherEmotions = time.time()




        #Modify and show photos
        smiley = smileyNeutral.copy()
        cv2.setWindowProperty('Camera', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Camera", frame)  			#Show you making emotional faces
        cv2.putText(smiley, "Score: "+str(score), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.putText(smiley, "Timer: "+str(round(time.time()-timeInitial, 1)), (20,240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        cv2.imshow("Smiley", smiley)            #Show the smiley to mimic




        #Save temporarily photo:
        if screen > 0:
            if time.time()-timeLastPhoto > time_play/(screen+1):
                timeLastPhoto = time.time()
                screen.append(frame)

        #Stop game if Q pressd or time exceed play time.
        if cv2.waitKey(1) & 0xFF == ord('q'):			#If you press Q, stop the while and so the capture
            break   

        elif cv2.waitKey(1) & 0xFF == ord('p'):			#If you press P, pass the smiley but lower your score
            score -= 1
            smiley, emotion = smileyRandom(emotion)
            smileyNeutral = smiley.copy()
            timeScoring = time.time()
            timeSinceOtherEmotions = time.time()
        

        elif time.time() - timeInitial > time_play:
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"Game ended ! You mimicked {score} emotions in {time_play} seconds !")
    if screen > 0:
        print("Some photos of your performance :")
        for photo in photos:
            plt.imshow(photo)
            plt.xticks([])
            plt.yticks([])
            plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Game of Facial Emotion Recognition')
    parser.add_argument('-p','--time-play', help='Duration of the game', required=False, default = 60, type=int)
    parser.add_argument('-m','--time-maintain', help='Duration required for maintaining emotion on screen to validate emotion', required=False, default = 0.3, type = float)
    parser.add_argument('-s','--screen', help='Number of photos screen during the game ', required=False, default = 0, type = int)
    args = vars(parser.parse_args())
    args["invincibleFrame"] = 0.5
    game(**args)
