'''
We will be using opencv, mediapipe and pyautogui to control the volume of the pc 
with our hands. The code is explained a bit with comments.
This project has more to do with using an already trained model to interact with the computer than 
training a new model. Hence no dataset was used in this task.
'''

#importing necessary libraries
import cv2
import mediapipe.python.solutions as mps
import pyautogui 
import numpy as np


x1=x2=y1=y2=0
cap = cv2.VideoCapture(0)
myhands = mps.hands.Hands()
lines = mps.drawing_utils

def distance(x1, y1, x2, y2): #to compute distance between fingers
    dist = np.sqrt((((x2-x1)**2) + ((y2-y1)**2)))//4
    return dist

while True: # an infinite while loop to interact with camera
    success, img = cap.read()
    img = cv2.flip(img, 1)
    frame_height, frame_width, frame_depth = img.shape
    rbg_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    output = myhands.process(rbg_img)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            lines.draw_landmarks(img, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
                if id == 8:
                    cv2.circle(img=img, center=(x,y),radius=8,color=(0,255,255),thickness=3)
                    x1 = x
                    y1 = y
                if id == 4:
                    cv2.circle(img=img, center=(x,y),radius=4,color=(0,0,255),thickness=3)
                    x2 = x
                    y2 = y
        dist = distance(x1,y1,x2,y2)
        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 5)
        if dist>40: # increase volume when fingers far apart
            pyautogui.press("volumeup")
        if dist<25: # decrease volume when fingers close together
            pyautogui.press("volumedown")
        
        
                
    cv2.imshow("Volume Control with Hands", img)
    key = cv2.waitKey(10) 
    if key == 27: # breaks the loop if ESC key is pressed
        break

cap.release()
cv2.destroyAllWindows()