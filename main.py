import cv2
import mediapipe as mp
import pyautogui
import threading
from maze import app
from flask import Flask
import time

running = True

def eye_tracking():
    global running
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()
    
    cv2.namedWindow('Face Mesh', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Face Mesh', cv2.WND_PROP_TOPMOST, 1)
    
    while running:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
            
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        if landmark_points:
            for face_landmarks in landmark_points:
                
                for id, landmark in enumerate(face_landmarks.landmark[474:478]):
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0))
                    if id == 1:
                        screen_x = screen_w / frame_w * x
                        screen_y = screen_h / frame_h * y
                        pyautogui.moveTo(screen_x, screen_y)
                
                left_eye_landmarks = [face_landmarks.landmark[145], face_landmarks.landmark[159]]
                for landmark in left_eye_landmarks:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 255))
                
                if (left_eye_landmarks[0].y - left_eye_landmarks[1].y) < 0.01:
                    pyautogui.click()
                    pyautogui.sleep(1)
        
        cv2.imshow('Face Mesh', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break
    
    cam.release()
    cv2.destroyAllWindows()

def flask_thread():
    app.run(debug=False, use_reloader=False) 

if __name__ == '__main__':
    eye_tracking_thread = threading.Thread(target=eye_tracking)
    eye_tracking_thread.start()
    
    flask_thread = threading.Thread(target=flask_thread)
    flask_thread.start()
    
    try:
        while running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        running = False
        
    eye_tracking_thread.join()
    flask_thread.join()