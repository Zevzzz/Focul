
import numpy as np
import matplotlib.pyplot as plt
import time
from enum import Enum
import cv2
from src import GUI, CameraIO, Landmarker, NeuralNet, Configs, Alerts, Balance

# Constants
MAX_UNFOC_TIME_FOR_ALERT = 10
DEFAULT_RECORDING_TIME_SEC = 60

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
bal = Balance.Balance('src\\data\\balance.txt')




def getLandmarkData():
    img = camIO.getImg()
    landmarkData = lmer.extractLandmarks(img)
    for landmark in landmarkData:
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
    if isFocused:
        allLandmarks = np.load('src\\data\\focusedLandmarks.npy')
    else:
        allLandmarks = np.load('src\\data\\unfocusedLandmarks.npy')

    allLandmarks = allLandmarks.tolist()
    # print('INITIAL: ' + str(allLandmarks))

    startTime = time.time()
    endTime = startTime + durationSec

    # print(allLandmarks.shape)

    while time.time() < endTime:
        amtDoneDeci = 1 - (endTime - time.time())/durationSec
        print(f'Percent Done: {round(amtDoneDeci * 100)}%')

        frameLandmarkData = getLandmarkData()
        if len(frameLandmarkData) > 0:
            allLandmarks.append(frameLandmarkData)


        if cv2.getWindowProperty('Focul', cv2.WND_PROP_VISIBLE) < 1:
            break

    if isFocused:
        Landmarker.writeLandmarks(np.array(allLandmarks), 'src\\data\\focusedLandmarks.npy')
    else:
        Landmarker.writeLandmarks(np.array(allLandmarks), 'src\\data\\unfocusedLandmarks.npy')


    print(f'\n'
          f'- - - - - - - - - - - - - - -\n'
          f'Total Clusters Collected\nFocused: '
          f'{len(np.load("src/data/focusedLandmarks.npy")):,}\n'
          f'Unfocused: {len(np.load("src/data/unfocusedLandmarks.npy")):,}\n'
          f'- - - - - - - - - - - - - - -\n')

    camIO.destroyAllWindows()
    camIO.release()


def gatherPointsFoc():
    samplingDurationSec = gui.popupAskSamplingDurationMin(DEFAULT_RECORDING_TIME_SEC / 60) * 60
    gatherPoints(True, samplingDurationSec)
def gatherPointsUnfoc():
    samplingDurationSec = gui.popupAskSamplingDurationMin(DEFAULT_RECORDING_TIME_SEC / 60) * 60
    gatherPoints(False, samplingDurationSec)

def resetRecordedData():
    if gui.popupAskClearData():
        np.save('src\\data\\focusedLandmarks.npy', np.empty((0, 33, 4)))
        np.save('src\\data\\unfocusedLandmarks.npy', np.empty((0, 33, 4)))
        gui.popupClearedData()




def displayDebugGraphs(val_acc):
    # Validation Accuracy vs Epochs
    epochs = np.arange(1, len(val_acc) + 1)
    plt.figure()
    plt.plot(epochs, val_acc, label="Validation Accuracy")
    plt.xlabel("Epochs")
    plt.ylabel("Validation Accuracy")
    plt.title("Validation Accuracy over Epochs")
    plt.legend()
    plt.show()

def trainModel():
    if gui.popupAskTrainModel():
        focLandmarks = Landmarker.readLandmarks('src\\data\\focusedLandmarks.npy')
        unfocLandmarks = Landmarker.readLandmarks('src\\data\\unfocusedLandmarks.npy')

        if len(focLandmarks) > 0 and len(unfocLandmarks) > 0:
            nn.trainModel(focLandmarks, unfocLandmarks)

            val_acc = np.load('src\\data\\TRAINING_HIST_VAL_ACC.npy')
            displayDebugGraphs(val_acc)
    gui.popupDoneTraining()



def displayFocusLog(focusSessionLog):
    # Extracting data
    focus_levels = np.array([entry[0] for entry in focusSessionLog])
    elapsed_times = np.array([entry[1] for entry in focusSessionLog])
    alerts = np.array([entry[2] for entry in focusSessionLog])

    # Determine session duration and appropriate moving average percentage
    session_duration = elapsed_times[-1] - elapsed_times[0]  # Total session duration in minutes
    session_minutes = int(session_duration)
    session_seconds = int((session_duration - session_minutes) * 60)

    if session_duration <= 5:
        movingAvgPerc = 10  # 10% for very short sessions
    elif session_duration <= 30:
        movingAvgPerc = 5   # 5% for moderate sessions
    else:
        movingAvgPerc = 2   # 2% for long sessions

    # Calculate the moving average with the determined window size
    window_size = max(1, int((movingAvgPerc / 100) * len(focus_levels)))  # Ensure window size is at least 1
    moving_avg_focus = np.convolve(focus_levels, np.ones(window_size) / window_size, mode='valid')

    # Adjust elapsed_times to match the length of moving average array
    adjusted_elapsed_times = elapsed_times[:len(moving_avg_focus)]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(adjusted_elapsed_times, moving_avg_focus, color='blue', label='Focus Level (Moving Average)')

    # Plot red dots where Has Been Alerted is True with larger size
    alert_times = elapsed_times[alerts]
    alert_focus_levels = focus_levels[alerts]
    plt.scatter(alert_times, alert_focus_levels, color='red', s=100, label='Alert Triggered', zorder=5)  # Increased size of red dots

    # Dashed horizontal line at y = 0.5
    plt.axhline(y=0.5, color='cyan', linestyle='--', linewidth=1.5, label='Focus Threshold (0.5)')

    # Labels, title, and axis limits with margin for y-axis
    plt.xlabel("Elapsed Session Time (minutes)")
    plt.ylabel("Focus Level (Moving Average)")
    plt.title(f"Focus Level Over Time (Session Duration: {session_minutes} min {session_seconds} sec)")
    plt.ylim(-0.1, 1.1)  # Setting y-axis limits with margin
    plt.legend()
    plt.grid(True)
    plt.show()




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

    focusSessionLog = []
    sessionStartTime = time.time()
    sessionEndTime = time.time()

    totalFocusTime = 0
    lastIterTime = time.time()

    while True:
        img = camIO.getImg()
        pred = predictWithModel(img)
        if not pred:
            continue

        focusLevel = 1 - pred
        hasAlerted = False


        if pred <= 0.5:
            lastFoc = time.time()
            totalFocusTime += (time.time() - lastIterTime)
        elif pred > 0.5 and abs(time.time() - lastFoc) > MAX_UNFOC_TIME_FOR_ALERT:
            hasAlerted = True
            totalFocusTime -= bal.PENALTY_MIN_FOR_ALERT * 60

            gui.popupFocusWarning()
            lastFoc = time.time()

        # Last iter timer for balance changes
        lastIterTime = time.time()

        # Add to log
        elapsedSessionTimeMin = (time.time() - sessionStartTime)/60
        focusSessionLog.append((focusLevel, elapsedSessionTimeMin, hasAlerted))


        predPerc = 50 + abs(50 - round(pred * 100))
        predMsg = ('Focused' if pred < 0.5 else 'Unfocused') + f' {str(predPerc)}%'
        cv2.putText(img, predMsg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 0), 2)
        camIO.showImg(img)

        # Check to exit loop
        try:
            if cv2.getWindowProperty("Focul", cv2.WND_PROP_VISIBLE) < 1:
                sessionEndTime = time.time()
                cv2.destroyAllWindows()
                camIO.release()

                # Show Focus Log
                displayFocusLog(focusSessionLog)

                # Modify/Show Balance
                sessionDurationMin = (sessionEndTime - sessionStartTime) / 60.0
                bal.changeBalWithTimeMin(sessionDurationMin)
                gui.popupShowBalance(bal.getBal())

                break
        except cv2.error:
            cv2.destroyAllWindows()
            camIO.release()
            break


def showBalance():
    gui.popupShowBalance(bal.getBal())

def updateBalanceManually():
    changeAmount = gui.popupAskBalanceUpdateAmt()
    bal.changeBal(changeAmount)
    gui.popupBalanceAmtUpdated()




if __name__ == '__main__':
    gui.initCommands(
        gatherPointsFoc,
        gatherPointsUnfoc,
        resetRecordedData,
        trainModel,
        startPredicting,
        showBalance,
        updateBalanceManually
    )
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























