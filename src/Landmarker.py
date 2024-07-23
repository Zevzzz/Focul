
import mediapipe as mp
import numpy as np


def writeLandmarks(landmarks, filepath):
    tempArr = []
    for cluster in landmarks:
        if cluster:
            tempArr.append(cluster)
    np.save(filepath, tempArr)


def readLandmarks(filepath):
    landmarks = np.load(filepath)
    return landmarks


class Landmarker:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose(static_image_mode = True, min_detection_confidence = 0.5)

    def extractLandmarks(self, img):
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img)
        landmarks = []
        if results.pose_landmarks:
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                x = landmark.x * img.shape[1]
                y = landmark.y * img.shape[0]
                z = landmark.z
                vis = landmark.visibility
                landmarks.append([x, y, z, vis])
        return landmarks

    def extractLandmarksFlattened(self, img):
        landmarks = np.array(self.extractLandmarks(img))
        landmarks = landmarks.reshape(len(landmarks), -1)
        landmarks = landmarks.flatten()
        return landmarks



