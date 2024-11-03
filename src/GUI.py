
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

def testCommand():
    print('TEST COMMAND RUN')


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Focul')
        self.root.configure(bg='#242424')

        WINDOW_WIDTH = 400
        WINDOW_HEIGHT = 600
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

        label1 = tk.Label(self.root, text='Welcome to', font=("Roboto", 20), fg='white', bg='#242424')
        label1.pack(pady=(30, 0))
        label2 = tk.Label(self.root, text='FOCUL', font=("Roboto", 30, 'bold'), fg='#00a8a8', bg='#242424')
        label2.pack(pady=(0, 40))


    def initCommands(self, recordFocCommand, recordUnfocCommand, resetRecordedDataCommand, trainModelCommand, monitorFocCommand, showBalance, updateBalance):
        self.button1 = tk.Button(self.root, text='Record Focused Video', font=("Roboto", 16), fg='white',
                            bg='#696969',
                            command=recordFocCommand)
        self.button1.pack(pady=8)

        self.button2 = tk.Button(self.root, text='Record Unfocused Video', font=("Roboto", 16), fg='white',
                            bg='#696969',
                            command=recordUnfocCommand)
        self.button2.pack(pady=8)

        self.button3 = tk.Button(self.root, text='Clear Recorded Data', font=("Roboto", 16), fg='white',
                                 bg='#5c2424',
                                 command=resetRecordedDataCommand)
        self.button3.pack(pady=8)

        self.button4 = tk.Button(self.root, text='Train Model with Recordings', font=("Roboto", 16), fg='white',
                            bg='#696969',
                            command=trainModelCommand)
        self.button4.pack(pady=(40, 8))

        self.button5 = tk.Button(self.root, text='Start Monitoring Focus', font=("Roboto", 16), fg='white',
                            bg='#016b6b',
                            command=monitorFocCommand)
        self.button5.pack(pady=8)

        self.button6 = tk.Button(self.root, text='Check Balance', font=("Roboto", 16), fg='white',
                                 bg='#696969',
                                 command=showBalance)
        self.button6.pack(side=tk.LEFT, padx=16)

        self.button7 = tk.Button(self.root, text='Update Balance', font=("Roboto", 16), fg='white',
                                 bg='#696969',
                                 command=updateBalance)
        self.button7.pack(side=tk.RIGHT, padx=16)

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

    def popupAskTrainModel(self):
        return messagebox.askokcancel('Train Model?', 'Confirm that you wish to begin training the model')

    def popupDoneTraining(self):
        messagebox.showinfo('FINISHED!', 'Training is complete!')

    def popupFocusWarning(self):
        messagebox.showwarning('Please remain focused!', 'Stay focused please!')

    def popupAskSamplingDurationMin(self, defaultSamplingDuration):
        inputtedDuration = simpledialog.askfloat("Input Sampling Duration (minutes)", "Enter duration (minutes):")
        if not inputtedDuration:
            return 0
        elif inputtedDuration <= 0:
            return defaultSamplingDuration
        else:
            return inputtedDuration



    def popupAskClearData(self):
        return messagebox.askokcancel('Clear Data?', 'Confirm that you wish to clear recorded landmark data')

    def popupClearedData(self):
        messagebox.showinfo('Landmarks Cleared', 'Recorded landmark data cleared')



    def popupShowBalance(self, balance):
        messagebox.showinfo('Balance Update', f'Your Updated Balance: {round(balance, 2)}$')

    def popupAskBalanceUpdateAmt(self):
        return simpledialog.askfloat('Input Balance Update Amount ($)', 'Enter Balance Update Amount ($): ')

    def popupBalanceAmtUpdated(self):
        messagebox.showinfo('Balance Updated', 'Balance Amount Updated Successfully!')




