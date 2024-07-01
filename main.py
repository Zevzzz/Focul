
import numpy as np
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
gui = GUI.GUI()
camIn = CameraIn.CameraIn()
lmer = Landmarker.Landmarker()
nn = NeuralNet.NeuralNet()
confs = Configs.Configs()
alerts = Alerts.Alerts()

def showImg(img):
    cv2.imshow('Focul', img)

    if cv2.waitKey(0) & 0xFF == 27:
        cv2.destroyAllWindows()


def getLandmarkData():
    img = camIn.captureImg()
    # showImg(img)
    return lmer.extractLandmarks(img)






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



if __name__ == '__main__':
    # camIn.startCap(0)
    # allLandmarks = []
    #
    # durationSec = 1
    #
    # startTime = time.time()
    # endTime = startTime + durationSec
    #
    # while time.time() < endTime:
    #     allLandmarks.append(getLandmarkData())
    #
    # Landmarker.writeLandmarks(allLandmarks, 'src/data/focusedLandmarks.npy')
    # print(f'Total Clusters Collected: {len(allLandmarks)}')


    # landmarks = Landmarker.readLandmarks('src/data/focusedLandmarks.npy')


    










