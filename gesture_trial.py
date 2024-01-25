import mediapipe as mp
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

model_path = "gesture_recog_new.task"
recognizer = vision.GestureRecognizer.create_from_model_path(model_path)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    
    ret, frame = cap.read()
    if not ret:
        break
    #frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    results = recognizer.recognize(img)
    top_gesture = results.gestures
    print(top_gesture)
    cv2.imshow('Hand Gesture Recognition', rgb_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
"""
    if top_gesture.score > 0.7 and top_gesture.category_name != 'none':
        print(f"Gesture recognized: {top_gesture.category_name} ({top_gesture.score})")
    else:
        print("Gesture not found")
    cv2.imshow('Hand Gesture Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
"""


