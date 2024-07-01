
from cv2 import VideoCapture, CAP_DSHOW

class CameraIn():

    cap = None

    def __init__(self):
        pass

    def startCap(self, cameraInd = 0):
        self.cap = VideoCapture(cameraInd, CAP_DSHOW)

        if not self.cap.isOpened():
            raise ValueError(f'Could not open camera with index {cameraInd}')


    def captureImg(self):
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






