
import cv2
while 1:
    if cv2.waitKey(0) & 0xFF== ord('q'):			#If you press Q, stop the while and so the capture
        break

    if cv2.waitKey(1) & 0xFF == ord('p'):			#If you press P, pass the smiley but lower your score
        score -= 1
        smiley, emotion = smileyRandom(emotion)
    print(1)
    cv2.waitKey(2)