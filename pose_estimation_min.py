import cv2
import mediapipe as mp
import time 

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
cap = cv2.VideoCapture('deadlift_form_positionest.mp4')
pTime =0
new_width = 640
new_height = 480
while True:
    success, img = cap.read()
    imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    print(results.pose_landmarks)
    if(results.pose_landmarks):
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate (results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx,cy = int(lm.x*w) , int(lm.y*h)
            cv2.circle(img, (cx,cy),5,(25,0,255),thickness=3)
    img_resized = cv2.resize(img, (new_width, new_height))
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img_resized , str(int(fps)),(70,50), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3 )
    cv2.imshow("Image",img_resized)
    cv2.waitKey(1)