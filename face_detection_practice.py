import mediapipe as mp
import cv2
import time
cap = cv2.VideoCapture('pose_est1.mp4')
mp.FaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mp.FaceDetection.FaceDetection(0.75)

newl = 1080
neww = 1080
ptime =0
while True:
    success, img =cap.read()
    ctime =time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    print(results)
    if results.detections:
        for id,detection in enumerate(results.detections):
            #mpDraw.draw_detection(img, detection)
            #print(detection.location_data.relative_bounding_box)
            bboxC = detection.location_data.relative_bounding_box
            #^this is the bounding box that comes from the class
            ih,iw,ic = img.shape 
            bbox = int(bboxC.xmin*iw) , int(bboxC.ymin*ih), int(bboxC.width*iw), int(bboxC.height*ih)
            cv2.rectangle(img,bbox,(255,0,0),2)
            cv2.putText(img, f'{int(detection.score[0]*100)}%',(bbox[0],bbox[1]-20),cv2.FONT_HERSHEY_PLAIN, 3,(0,255,0),2)
    img_resized = cv2.resize(img, (neww, newl))
    cv2.putText(img_resized , str(int(fps)) ,(70,50) , cv2.FONT_HERSHEY_COMPLEX_SMALL, 3 , (0,255,0) ,4 )
    cv2.imshow("Image",img_resized)
    
    cv2.waitKey(10)