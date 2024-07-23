import cv2
from cv2 import VideoCapture, CAP_DSHOW, imshow, waitKey, destroyAllWindows

class CameraIO:

    cap = None

    def __init__(self):
        pass

    def showImg(self, img):
        imshow('Focul', img)

        if waitKey(33) & 0xFF == 27:
            destroyAllWindows()

    def startCap(self, cameraInd = 0):
        self.cap = VideoCapture(cameraInd, CAP_DSHOW)

        if not self.cap.isOpened():
            raise ValueError(f'Could not open camera with index {cameraInd}')


    def getImg(self):
        if self.cap:
            ret, img = self.cap.read()
            return img
        else:
            raise ValueError('No capture found')

    def release(self):
        if self.cap:
            self.cap.release()
        else:
            raise ValueError('No capture found')

    def destroyAllWindows(self):
        cv2.destroyAllWindows()






