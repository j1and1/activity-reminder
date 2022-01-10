from time import sleep
import cv2
import mediapipe as mp 
import threading

class PoseDetector:

    def __init__(self):
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()
        self.mpDraw = mp.solutions.drawing_utils

    def detect(self, image_rgb):
        self.image_rgb = image_rgb
        self.results = self.pose.detect(image_rgb)
        return self.results.pose_landmarks

    def find_landmark(self, landmark_id):
        results = self.results.pose_landmarks
        if results:
            h, w, c = self.image_rgb.shape
            for id, lm in enumerate(results):
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == landmark_id:
                    return cx, cy #landmark found return position
        return None, None # landmark not found

    def draw_position(self):
        self.mpDraw.draw_landmarks(self.image_rgb, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

class ComputerVision:

    def __init__(self, cfg, on_frame_ready):
        self.on_frame_ready = on_frame_ready
        self.running = True
        self.cap = cv2.VideoCapture(cfg.camera)

        self.process = threading.Thread(target=self.main_loop)
        self.process.start()

    def main_loop(self):
        while self.running:
            ret, image = self.cap.read()
            #convert to mediapipe color format
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.on_frame_ready(ret, image, rgb)
            sleep(0.04)

        self.cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False
        self.process.join()

class SquatDetector:

    def __init__(self, cfg, on_frame_ready, on_detected):
        pass