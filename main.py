import cv2
import mediapipe as mp
import pyautogui
import threading
from maze import app 

def eye_tracking():
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()

    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            print("Failed to grab frame")
            break

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
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    threading.Thread(target=eye_tracking, daemon=True).start()
    
    app.run(debug=True)
