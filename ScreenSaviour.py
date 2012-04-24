from Tkconstants import CENTER
import Tkinter
#import Image, ImageTk
from multiprocessing import Process
import ctypes
import time
import sys

class ScreenSaviour(Tkinter.Tk):
    """
    A very simple Tkinter program to move the mouse in windows at some interval, primarily to disable a windows screen saver.
    Useful if you need it in a pinch.
    """
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.clickInterval = 840 #14 minutes
        print "Initializing ScreenSaviour"
        self.create_interface()

    def create_interface(self):
        self.grid()

        #Setup Labels
        self.clickIntervalLabelVariable = Tkinter.StringVar()
        self.clickIntervalLabel = Tkinter.Label(self,padx=3,pady=3,textvariable=self.clickIntervalLabelVariable,anchor="w",fg="black")
        self.clickIntervalLabel.grid(column=0,row=0,columnspan=1,sticky='W')
        self.clickIntervalLabelVariable.set(u"Enter click interval here:")

        #Setup Labels
        self.intervalErrorLabelVariable = Tkinter.StringVar()
        self.intervalErrorLabel = Tkinter.Label(self,padx=3,pady=3,textvariable=self.intervalErrorLabelVariable,anchor="w",fg="red")
        self.intervalErrorLabel.grid(column=0,row=1,columnspan=1,sticky='W')
        self.intervalErrorLabelVariable.set(u" ")

        #Setup Entries
        self.clickIntervalVariable = Tkinter.StringVar()
        self.clickIntervalEntry = Tkinter.Entry(self,textvariable=self.clickIntervalVariable)
        self.clickIntervalEntry.grid(column=1,row=0,columnspan=2,sticky='W')
        self.clickIntervalEntry.bind("<Return>", self.OnPressEnter)
        self.clickIntervalVariable.set(u""+str(self.clickInterval))

        #image
#        image = Image.open("saviour.jpg")
#        saviour = ImageTk.PhotoImage(image)
#        ourSaviour = Tk.Label(image=saviour)
#        ourSaviour.image = saviour

        #Setup buttons
        start_button = Tkinter.Button(self,text=u"Start!",command=self.OnStartButtonClick)
        start_button.grid(columnspan=2,column=1,row=2)

        stop_button = Tkinter.Button(self,text=u"Stop!",command=self.OnStopButtonClick)
        stop_button.grid(columnspan=2,column=2,row=2)

        exit_button = Tkinter.Button(self,text=u"Exit!",command=self.OnExitButtonClick)
        exit_button.grid(columnspan=2,column=3,row=2)

    def OnStartButtonClick(self):
        self.extractVariables()
        self.start_loop()

    def OnExitButtonClick(self):
        print "Exit"
        try:
            self.process.join(1)
            self.process.terminate()
        except Exception:
            pass
        finally:
            sys.exit()

    def OnStopButtonClick(self):
        self.stop_loop()

    def OnPressEnter(self,event):
        self.extractVariables()
        self.start_loop()

    def extractVariables(self):
        self.clickInterval = self.clickIntervalVariable.get()

    def start_loop(self):
        print "Starting ScreenAlive clickInterval=", self.clickInterval
        if int(self.clickInterval) < 10:
            self.intervalErrorLabelVariable.set(u"You don't want a click interval this low!")
            return
        self.intervalErrorLabelVariable.set(u"")
        self.process = self.process = Process(target=runTarget,args=(self.clickInterval,))
        self.process.start()

    def stop_loop(self):
        print "Stopping ScreenAlive clickInterval=", self.clickInterval
        try:
            self.process.join(timeout=1)
            self.process.terminate()
        except Exception:
            pass

def runTarget(click_interval):
    print "Run Target"
    while True:
        print "clickity click"
        ctypes.windll.user32.SetCursorPos(100, 20)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up
        time.sleep(int(click_interval))
    print "Shutting down"
    sys.exit()


if __name__ == "__main__":
    app = ScreenSaviour(None)
    app.title('ScreenSaviour')
    app.mainloop()


