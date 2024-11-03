import cv2
import mediapipe as mp
import pyautogui
import threading
from maze import app
import time

running = True

def eye_tracking():
    global running
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()
    
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
                    
                    if id == 1:
                        screen_x = screen_w / frame_w * x
                        screen_y = screen_h / frame_h * y
                        pyautogui.moveTo(screen_x, screen_y)
                        print(f"Cursor moved to X: {screen_x}, Y: {screen_y}")  # Logging movement
                
                # Detecting a blink and logging it
                left_eye_landmarks = [face_landmarks.landmark[145], face_landmarks.landmark[159]]
                if (left_eye_landmarks[0].y - left_eye_landmarks[1].y) < 0.01:
                    pyautogui.click()
                    print("Eye blink detected, click registered")
                    pyautogui.sleep(1)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break
    
    cam.release()

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
