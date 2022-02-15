from time import monotonic_ns

from numpy.core.arrayprint import _make_options_dict


def smileyRandom(emotionToDodge):
    #Return a random smiley and te emotion associated

    import cv2
    import random
    from config import emotions

    emotionNbr = random.randrange(0,6)
    emotion = emotions[emotionNbr]
    if emotion == emotionToDodge: return smileyRandom(emotion)
    smileyImagePath = "data/smileys/"+emotion+".png"
    smiley = cv2.imread(smileyImagePath)
    return smiley, emotion


def game(playTime = 30, dt_required=0.5, n_photos=None, invincibleFrame=0.5):
    #Play a game.

    # playTime : durée de jeu
    # invincibleFrame : durée minimale entre deux émotions
    # dt_required : durée minimal nécessaire pour valider une émotion
    # n_photos : nombre de photos prises

    #Use your camera for processing the video. Stop by pressing Q
    import cv2
    import matplotlib.pyplot as plt
    import imageProcess as ip
    import time


    cap = cv2.VideoCapture(0)   #0 means we capture the first camera, your webcam probably
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
        
        
        if time.time()-timeSinceOtherEmotions > dt_required:    #If emotions maintained for dt seconds, score is increased and a new smiley is generated
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
        cv2.imshow("Caméra", frame)  			#Show you making emotional faces
        cv2.putText(smiley, "Score: "+str(score), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.putText(smiley, "Timer: "+str(round(time.time()-timeInitial, 1)), (20,240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        cv2.imshow("Smiley", smiley)            #Show the smiley to mimic




        #Save temporarily photo:
        if n_photos is not None:
            if time.time()-timeLastPhoto > playTime/(n_photos+1):
                timeLastPhoto = time.time()
                photos.append(frame)

        #Stop game if Q pressd or time exceed play time.
        if cv2.waitKey(1) & 0xFF == ord('q'):			#If you press Q, stop the while and so the capture
            break   

        elif cv2.waitKey(1) & 0xFF == ord('p'):			#If you press P, pass the smiley but lower your score
            score -= 1
            smiley, emotion = smileyRandom(emotion)
            smileyNeutral = smiley.copy()
            timeScoring = time.time()
            timeSinceOtherEmotions = time.time()
        

        elif time.time() - timeInitial > playTime:
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"Jeu terminé ! Vous avez imité {score} emotions en {playTime} secondes !")
    if n_photos is not None:
        print("Voici quelques photos prises lors de votre performance =)")
        for photo in photos:
            plt.imshow(photo)
            plt.xticks([])
            plt.yticks([])
            plt.show()

if __name__ == "__main__":
    game(600, invincibleFrame=0.5, dt_required=0.3, n_photos=10)
