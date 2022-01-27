from time import sleep
import cv2
import mediapipe as mp 
import threading
import math

class PoseDetector:

    def __init__(self):
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(min_detection_confidence = 0.65)
        self.mpDraw = mp.solutions.drawing_utils

    def detect(self, image_rgb):
        self.image_rgb = image_rgb
        self.results = self.pose.process(image_rgb)
        return self.results.pose_landmarks

    def find_landmark(self, landmark_id):
        results = self.results.pose_landmarks
        if results:
            h, w, c = self.image_rgb.shape
            for id, lm in enumerate(results.landmark):
                if id == landmark_id:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    #print(f"Landmark with {id} found at {cx} {cy}")
                    return cx, cy #landmark found return position
        raise Exception(f"Landmark not found with {landmark_id}") # landmark not found throw

    def draw_position(self, image):
        self.mpDraw.draw_landmarks(image, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

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
        # self.process.join()

class SquatDetector:

    def __init__(self, cfg, on_frame_ready, on_detected):
        self.on_frame_ready = on_frame_ready
        self.on_detected = on_detected
        self.cfg = cfg

        self.vision = None
        self.last_angle = 0

        self.detector = PoseDetector()

    def start(self):
        if self.vision is not None:
            self.vision.stop()
        self.vision = ComputerVision(self.cfg, self.frame_ready)

    def stop(self):
        if self.vision is not None:
            self.vision.stop()

    def wait(self):
        if self.vision is not None:
            self.vision.process.join()

    def frame_ready(self, ret, image, image_rgb):
        if not ret:
            return
        self.detector.detect(image_rgb)
        self.detector.draw_position(image)

        self.on_frame_ready(image)

        #get the positions of all needed limbs
        #left side
        angle_left = 180
        try:
            ankle_x, ankle_y = self.detector.find_landmark(self.detector.mpPose.PoseLandmark.LEFT_ANKLE)
            knee_x, knee_y = self.detector.find_landmark(self.detector.mpPose.PoseLandmark.LEFT_KNEE)
            hip_x, hip_y = self.detector.find_landmark(self.detector.mpPose.PoseLandmark.LEFT_HIP)

            angle_left = math.degrees(math.atan2(hip_x - knee_x, hip_y - knee_y) - math.atan2(ankle_x - knee_x, ankle_y - knee_y))
            angle_left = abs(angle_left)
            # print(f'Current LEFT angle is: {angle_left}')
        except Exception as e:
            #print (str(e))
            pass

        #right side
        angle_right = 180
        try:
            ankle_x, ankle_y = self.detector.find_landmark(self.detector.mpPose.PoseLandmark.RIGHT_ANKLE)
            knee_x, knee_y = self.detector.find_landmark(self.detector.mpPose.PoseLandmark.RIGHT_KNEE)
            hip_x, hip_y = self.detector.find_landmark(self.detector.mpPose.PoseLandmark.RIGHT_HIP)

            angle_right = math.degrees(math.atan2(hip_x - knee_x, hip_y - knee_y) - math.atan2(ankle_x - knee_x, ankle_y - knee_y))
            angle_right = abs(angle_right)
            # print(f'Current RIGHT angle is: {angle_right}')
        except Exception as e:
            #print (str(e))
            pass
        
        angle = (angle_right + angle_left) / 2.0
        if angle <= 90:
            if self.last_angle >= 175:
                self.on_detected(True, angle) #let parent know that we're squatting
                self.last_angle = angle
        elif angle >= 175:
            if self.last_angle <= 90:
                self.on_detected(False, angle) # let parent class know that we're stanging
                self.last_angle = angle

