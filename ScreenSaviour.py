import Tkinter
from multiprocessing import Process
import ctypes
import time

RUNNING = True

class ScreenSaviour(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.clickInterval = 0
        self.totalRuntime = 0
        self.RUNNING = True
        print "Initializing ScreenSaviour"
        self.create_interface()

    def create_interface(self):
        self.grid()

        #Setup Labels
        self.clickIntervalLabelVariable = Tkinter.StringVar()
        self.clickIntervalLabel = Tkinter.Label(self,textvariable=self.clickIntervalLabelVariable,anchor="w",fg="black")
        self.clickIntervalLabel.grid(column=0,row=0,columnspan=1,sticky='EW')
        self.clickIntervalLabelVariable.set(u"Enter click interval here:")

        self.totalRuntimeLabelVariable = Tkinter.StringVar()
        self.totalRuntimeLabel = Tkinter.Label(self,textvariable=self.totalRuntimeLabelVariable,anchor="w",fg="black")
        self.totalRuntimeLabel.grid(column=0,row=1,columnspan=1,sticky='EW')
        self.totalRuntimeLabelVariable.set(u"Enter total runtime here:")

        #Setup Entries
        self.clickIntervalVariable = Tkinter.StringVar()
        self.clickIntervalEntry = Tkinter.Entry(self,textvariable=self.clickIntervalVariable)
        self.clickIntervalEntry.grid(column=3,row=0,sticky='EW')
        self.clickIntervalEntry.bind("<Return>", self.OnPressEnter)
        self.clickIntervalVariable.set(u"0")

        self.totalRuntimeVariable = Tkinter.StringVar()
        self.totalRuntimeEntry = Tkinter.Entry(self,textvariable=self.totalRuntimeVariable)
        self.totalRuntimeEntry.grid(column=3,row=1,sticky='EW')
        self.totalRuntimeEntry.bind("<Return>", self.OnPressEnter)
        self.totalRuntimeVariable.set(u"0")

        #Setup buttons
        start_button = Tkinter.Button(self,text=u"Start!",command=self.OnStartButtonClick)
        start_button.grid(column=1,row=4)

        stop_button = Tkinter.Button(self,text=u"Stop!",command=self.OnStopButtonClick)
        stop_button.grid(column=2,row=4)

    def OnStartButtonClick(self):
        self.extractVariables()
#        self.entry.focus_set()
#        self.entry.selection_range(0, Tkinter.END)
        self.start_loop()

    def OnStopButtonClick(self):
        self.extractVariables()
#        self.entry.focus_set()
#        self.entry.selection_range(0, Tkinter.END)
        self.stop_loop()

    def OnPressEnter(self,event):
        self.extractVariables()
#        self.entry.focus_set()
#        self.entry.selection_range(0, Tkinter.END)
        self.start_loop()

    def extractVariables(self):
        self.clickInterval = self.clickIntervalVariable.get()
        self.totalRuntime = self.totalRuntimeVariable.get()

    def start_loop(self):
        print "Starting ScreenAlive", self.clickInterval, self.totalRuntime
        self.process = self.process = Process(target=runTarget,args=(self.clickInterval,self.totalRuntime))
        self.process.start()

    def stop_loop(self):
        print "Stopping ScreenAlive", self.clickInterval, self.totalRuntime
        timeout = int(self.clickInterval)+10
        self.process.join(timeout=timeout)
        self.process.terminate()

def runTarget(click_interval, totalRuntime):
    print "Run Target"
    while RUNNING:
        ctypes.windll.user32.SetCursorPos(100, 20)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up
        time.sleep(100)

if __name__ == "__main__":
    app = ScreenSaviour(None)
    app.title('ScreenSaviour')
    app.mainloop()


