
import tkinter as tk
from tkinter import messagebox

def testCommand():
    print('TEST COMMAND RUN')


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Focul')
        self.root.configure(bg='#242424')

        WINDOW_WIDTH = 400
        WINDOW_HEIGHT = 500
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

        label1 = tk.Label(self.root, text='Welcome to', font=("Roboto", 20), fg='white', bg='#242424')
        label1.pack(pady=(30, 0))
        label2 = tk.Label(self.root, text='FOCUL', font=("Roboto", 30, 'bold'), fg='#00a8a8', bg='#242424')
        label2.pack(pady=(0, 90))


    def initCommands(self, recordFocCommand, recordUnfocCommand, trainModelCommand, monitorFocCommand):
        self.button1 = tk.Button(self.root, text='Record Focused Video', font=("Roboto", 16), fg='white',
                            bg='#696969',
                            command=recordFocCommand)
        self.button1.pack(pady=8)

        self.button2 = tk.Button(self.root, text='Record Unfocused Video', font=("Roboto", 16), fg='white',
                            bg='#696969',
                            command=recordUnfocCommand)
        self.button2.pack(pady=8)

        self.button3 = tk.Button(self.root, text='Train Model with Recordings', font=("Roboto", 16), fg='white',
                            bg='#696969',
                            command=trainModelCommand)
        self.button3.pack(pady=8)

        self.button4 = tk.Button(self.root, text='Start Monitoring Focus', font=("Roboto", 16), fg='white',
                            bg='#016b6b',
                            command=monitorFocCommand)
        self.button4.pack(pady=(25, 10))

    # def getToggleMonitoringButtonStateIsActive(self):
    #     return self.button4.cget('text') == 'Stop Monitoring Focus'
    #
    # def toggleStartMonitoringFocusButtonText(self):
    #     if self.getToggleMonitoringButtonStateIsActive():
    #         self.button4.config(text='Start Monitoring Focus', bg='#016b6b')
    #     else:
    #         self.button4.config(text='Stop Monitoring Focus', bg='#009118')


    def startGUI(self):
        self.root.mainloop()

    def closeWindow(self):
        self.root.destroy()


    def popupFocusWarning(self):
        messagebox.showwarning('Please remain focused!', 'Stay focused please!')







