
import numpy as np
import matplotlib.pyplot as plt
import time
from enum import Enum
import cv2
from src import GUI, CameraIO, Landmarker, NeuralNet, Configs, Alerts

# Constants
MAX_UNFOC_TIME_FOR_ALERT = 10
RECORDING_TIME_SEC = 60

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
camIO = CameraIO.CameraIO()
lmer = Landmarker.Landmarker()
nn = NeuralNet.NeuralNet()
# confs = Configs.Configs()
# alerts = Alerts.Alerts()




def getLandmarkData():
    img = camIO.getImg()
    landmarkData = lmer.extractLandmarks(img)
    for landmark in landmarkData:
        print(landmark)
        img = cv2.circle(img, (int(landmark[0]), int(landmark[1])), 3, (255, 0, 0), 5)
    camIO.showImg(img)
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


def gatherPoints(isFocused, durationSec):
    camIO.startCap(0)
    allLandmarks = []

    startTime = time.time()
    endTime = startTime + durationSec

    while time.time() < endTime:
        allLandmarks.append(getLandmarkData())

    if isFocused:
        Landmarker.writeLandmarks(allLandmarks, 'src\\data\\focusedLandmarks.npy')
    else:
        Landmarker.writeLandmarks(allLandmarks, 'src\\data\\unfocusedLandmarks.npy')
    print(f'Total Clusters Collected: {len(allLandmarks)}')

    camIO.destroyAllWindows()
    camIO.release()


def gatherPointsFoc():
    gatherPoints(True, RECORDING_TIME_SEC)
def gatherPointsUnfoc():
    gatherPoints(False, RECORDING_TIME_SEC)


def trainModel():
    if gui.askStartTraining():
        focLandmarks = Landmarker.readLandmarks('src\\data\\focusedLandmarks.npy')
        print(focLandmarks)
        print(len(focLandmarks))

        unfocLandmarks = Landmarker.readLandmarks('src\\data\\unfocusedLandmarks.npy')
        print(unfocLandmarks)
        print(len(unfocLandmarks))

        if len(focLandmarks) > 0 and len(unfocLandmarks) > 0:
            nn.trainModel(focLandmarks, unfocLandmarks)
            trainingHist = np.load('src\\data\\TRAINING_HIST_VAL_ACC.npy')

            # plt.plot(trainingHist)
            # plt.show()
        gui.popupDoneTraining()


def predictWithModel(img):
    try:
        landmarks = lmer.extractLandmarksFlattened(img)
        nn.loadModel()
        return nn.predict(landmarks)[0][0]
    except ValueError or AttributeError:
        print('No Landmarks Found')
        return None

def startPredicting():
    camIO.startCap()
    lastFoc = time.time()

    while True:
        img = camIO.getImg()
        print(img.shape)
        pred = predictWithModel(img)
        if not pred:
            continue

        # Response to unfoc
        # Foc
        if pred <= 0.5:
            lastFoc = time.time()
        elif pred > 0.5 and abs(time.time() - lastFoc) > MAX_UNFOC_TIME_FOR_ALERT:
            gui.popupFocusWarning()
            lastFoc = time.time()


        predPerc = 50 + abs(50 - round(pred * 100))
        predMsg = ('Focused' if pred < 0.5 else 'Unfocused') + f' {str(predPerc)}%'
        cv2.putText(img, predMsg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 0), 2)
        camIO.showImg(img)

        # Check to exit loop
        try:
            if cv2.getWindowProperty('Focul', 0) == -1:
                cv2.destroyAllWindows()
                camIO.release()
                break
        except cv2.error:
            cv2.destroyAllWindows()
            camIO.release()
            break


if __name__ == '__main__':
    gui.initCommands(gatherPointsFoc, gatherPointsUnfoc, trainModel, startPredicting)
    gui.startGUI()



    # camIO.startCap(0)

    # gatherPoints(False, 60)

    # trainModel()

    # while True:
    #     img = camIO.captureImg()
    #     pred = predictWithModel(img)
    #     if not pred:
    #         continue
    #
    #     predPerc = 50 + abs(50 - round(pred * 100))
    #     predMsg = ('Focused' if pred < 0.5 else 'Unfocused') + f' {str(predPerc)}%'
    #     cv2.putText(img, predMsg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 0), 2)
    #     camIO.showImg(img)

