import cv2
import mediapipe as mp
import time
import numpy as np
import math
import hand_practice_module as htm
import pycaw
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()

volrange = volume.GetVolumeRange()
minVol = volrange[0]
maxVol = volrange[1]

wcam=640
hcam=480

cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ptime =0
detector =  htm.handDetector()
vol=0
volbar=400
while True :
    success,img =cap.read()
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img=detector.findHands(imgRGB)
    lmlist = detector.findPosition(imgRGB,draw=True)
    if(len(lmlist)!=0):
        #print(lmlist[2]) 
        cen1=(lmlist[4][1]+lmlist[8][1])//2
        cen2=(lmlist[8][2]+lmlist[4][2])//2
        cv2.circle(imgRGB,(lmlist[4][1],lmlist[4][2]),14,(2,2,24),thickness=3)

        cv2.circle(imgRGB,(lmlist[8][1],lmlist[8][2]),14,(2,2,24),thickness=3)
        cv2.circle(imgRGB,(cen1,cen2),14,(2,2,24),thickness=3)
        cv2.line(imgRGB,(lmlist[4][1],lmlist[4][2]),(lmlist[8][1],lmlist[8][2]) ,(255,0,0),3)
        length = math.hypot(lmlist[8][1]-lmlist[4][1] , lmlist[8][2]-lmlist[4][2])
        print(length)
        vol =np.interp(length, [30,240] , [minVol,maxVol])
        volbar=np.interp(length , [30,240] , [400,150])
        volume.SetMasterVolumeLevel(vol, None)
        
        if(length<45):
            cv2.circle(imgRGB,(cen1,cen2),14,(2,2,255),cv2.FILLED)
    cv2.rectangle(imgRGB,(50,150) , (85,400) ,(0,255,0) , 4)
    cv2.rectangle(imgRGB, (50,int(volbar)) ,(85,400) , (0,255,0) , cv2.FILLED )
    cv2.circle(imgRGB, (50,150) , 5 ,(25,0,0) , thickness = 3 )
    cv2.circle(imgRGB, (85,400) , 5 ,(255,0,0) , thickness = 3 )
    cv2.putText(imgRGB, f'FPS:{int(fps)}', (50,70) , cv2.FONT_HERSHEY_COMPLEX , 1 , (255,0,0),3)
    cv2.imshow("Image",imgRGB)
    
    cv2.waitKey(1)