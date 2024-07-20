
import numpy as np
import matplotlib.pyplot as plt
import time
from enum import Enum
from src import GUI, CameraIn, Landmarker, NeuralNet, Configs, Alerts
import cv2

# App states
class AppPageState(Enum):
    HOME = 0
    COLLECT_FOC = 1
    COLLECT_UNFOC = 2
    TRAINING = 3
    RUNNING = 4
    CONFIG = 5
appPageState = AppPageState.HOME

# Init components
# gui = GUI.GUI()
camIn = CameraIn.CameraIn()
lmer = Landmarker.Landmarker()
nn = NeuralNet.NeuralNet()
# confs = Configs.Configs()
# alerts = Alerts.Alerts()

def showImg(img):
    cv2.imshow('Focul', img)

    if cv2.waitKey(33) & 0xFF == 27:
        cv2.destroyAllWindows()


def getLandmarkData():
    img = camIn.captureImg()
    landmarkData = lmer.extractLandmarks(img)
    for landmark in landmarkData:
        print(landmark)
        img = cv2.circle(img, (int(landmark[0]), int(landmark[1])), 3, (255, 0, 0), 5)
    showImg(img)
    return landmarkData





# while True:
#     match appPageState:
#         case AppPageState.HOME:
#             pass
#         case AppPageState.COLLECT_FOC:
#             pass
#         case AppPageState.COLLECT_UNFOC:
#             pass
#         case AppPageState.TRAINING:
#             pass
#         case AppPageState.RUNNING:
#             pass
#         case AppPageState.CONFIG:
#             pass


def gatherPoints():
    camIn.startCap(0)
    allLandmarks = []

    durationSec = 60

    startTime = time.time()
    endTime = startTime + durationSec

    while time.time() < endTime:
        allLandmarks.append(getLandmarkData())

    Landmarker.writeLandmarks(allLandmarks, 'src/data/unfocusedLandmarks.npy')
    print(f'Total Clusters Collected: {len(allLandmarks)}')

def trainModel():
    focLandmarks = Landmarker.readLandmarks('src/data/focusedLandmarks.npy')
    print(focLandmarks)
    print(len(focLandmarks))

    unfocLandmarks = Landmarker.readLandmarks('src/data/unfocusedLandmarks.npy')
    print(unfocLandmarks)
    print(len(unfocLandmarks))

    nn.trainModel(focLandmarks, unfocLandmarks)
    trainingHist = np.load('TRAINING_HIST_VAL_ACC.npy')

    plt.plot(trainingHist)
    plt.show()

def predictWithModel():
    camIn.startCap(0)
    while True:
        img = camIn.captureImg()
        showImg(img)

        try:
            landmarks = lmer.extractLandmarksFlattened(img)
        except ValueError:
            print('No Landmarks Found')
            continue

        print(nn.predict(landmarks))




if __name__ == '__main__':
    # gatherPoints()

    # trainModel()

    predictWithModel()













