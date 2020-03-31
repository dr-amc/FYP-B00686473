import cv2
import numpy as np
import os 
# using a haarcascade to detect my face and greets me with a welcome message
# prompts any new users that it doesnt recognise 

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/share/rpi-code/FacialRecognitionProject/trainer/trainer.yml')
cascadePath = "/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Eamon'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0, cv2.CAP_V4L)
cam.set(3, 960) # set video widht
cam.set(4, 720) # set video height

# Define min window size to be recognized as a face
minW = .25*cam.get(3) 
minH = .25*cam.get(4) 

intro = False
c = 10
d = 5

while True:

    ret, img = cam.read()
    # img = cv2.flip(img, -1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        # minSize = (int(minW), int(minH)),
        minSize = (200, 20)
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 75):
            print(id)
            id_num = id
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            print(id)
            print(c)
            
            if intro is False:
                os.system("mplayer -ao alsa -noconsolecontrols /home/pi/share/hello_Eamon.mp3") # Hello Eamon output
                intro = True
                c = 0
                
            else:           
                if c > 9:
                    if id_num == 1:
                        os.system("mplayer -ao alsa -noconsolecontrols /home/pi/share/return_Eamon.mp3") 
                        c = 0
                c += 1
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
            
            if d > 4:
                os.system("mplayer -ao alsa -noconsolecontrols /home/pi/share/unknown_Eamon.mp3") # If a face is detected that is not Eamon
                d = 0            
            
            d += 1
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,0,0), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (0,0,255), 2)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
