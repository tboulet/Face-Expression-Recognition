

def videoCapture():

    #Use your camera for processing the video. Stop by pressing Q
    import cv2
    import imageProcess as ip

    cap = cv2.VideoCapture(0)   #0 means we capture the first camera, your webcam probably

    while cap.isOpened():		 #or while 1. cap.isOpened() is false if there is a problem
        ret, frame = cap.read()  #Read next video frame, stop if frame not well read
        if not ret: break

        ip.imageProcess(frame)                          #Process frame

        cv2.imshow("Image", frame)  			#Show processed image in a window

        if cv2.waitKey(1) & 0xFF == ord('q'):			#If you press Q, stop the while and so the capture
            break       

    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    videoCapture()