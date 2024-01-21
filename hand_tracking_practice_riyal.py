import cv2
import mediapipe as mp 
from mediapipe import solutions
import time 
cap = cv2.VideoCapture(0)

mpHands=  mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
cTime=0
pTime=0

while True:
    success, img =cap.read()
    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    
    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    if(results.multi_hand_landmarks):
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                h, w, c = imgRGB.shape
                cx,cy =int(lm.x*w) , int (lm.y*h)
                print(id, "|" , cx , "|" ,cy )
                
                if(id==0):
                    cv2.circle(imgRGB, (cx,cy),25,(255,0,255), 2)
                
                #the above prints the location of the hand points , of which there are a total of 21;
            mpDraw.draw_landmarks(imgRGB, handLms , mpHands.HAND_CONNECTIONS)
    #print(results.multi_hand_landmarks!=None)
    cTime = time.time()
    fps  = 1/(cTime-pTime)
    pTime = cTime
    
    
    cv2.putText(imgRGB, str(results.multi_hand_landmarks!=None) , (10,80) ,cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.putText(imgRGB, str(int(fps)) , (180,80) ,cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    
    cv2.imshow("Image", imgRGB)
    if cv2.waitKey(1) & 0xFF == ord('m'):
        break
    