from os import listdir

from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import tkinter as tk
from threading import Thread
import globals
import h5py
import paramiko
import os
import shutil

class AsyncTest(Thread):
    def __init__(self, addressFile, name, group, typeTest, tChannel, samples):
        super().__init__()
        self.addressFile = addressFile
        self.name = name
        self.group = group
        self.typeTest = typeTest
        self.tChannel = tChannel
        self.samples = samples

    def run(self):
        globals.threadComm = "test"

        while True:
            # Mientras no se reciba de la FPGA que se ha terminado el test no se hace nada
            if globals.testDone:
                break

        remotePath = '/media/sd-mmcblk0p1/files'
        path = 'FILES'

        fileExists = os.path.exists(path)
        if fileExists:
            shutil.rmtree(path)
            os.mkdir(path)
        else:
            os.mkdir(path)

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('192.168.10.60', username='root', password='root')

        sftp = client.open_sftp()

        for remoteFile in sftp.listdir(remotePath):
            if remoteFile[0:12] == 'afe5808_out_':
                file = open("FILES/" + remoteFile, "w")  # Creamos nuevo fichero local
                file.close()
                sftp.get(remotePath + "/" + remoteFile, "FILES/" + remoteFile)

        sftp.close()
        client.close()

        column = 0
        row = 1

        with h5py.File(self.addressFile, "a") as f:
            grp = f.require_group(self.group)
            # Change the samples with self.parent.sampl + num of extra rows needed
            # Always at least 1 extra row obligatory
            # Another extra row for the type of test on the top

            if self.typeTest == 2:
                print("Hay que crear aquí 64 columnas")
                dset = grp.create_dataset(self.name + "Results", (int(self.samples) + 2, 64), dtype='f')
                for i in range(8):
                    dset[0, 1 + 8 * i] = i
                # pathFinal = pathRR
            else:
                dset = grp.create_dataset(self.name + "Results", (int(self.samples) + 2, 8), dtype='f')
                dset[0, 1] = self.tChannel
                # pathFinal = path

            dset[0, 0] = self.typeTest
            dset.attrs['Results'] = 1
            for file in listdir("FILES"):
                with open("FILES" + "/" + file) as f:
                    for line in f:
                        if line:
                            dset[row, column] = (float(line)/8190.5) - 1
                            row = row + 1
                column = column + 1
                row = 1


def notClosing():
    pass
    # print("By doing this the user can not cancel de process and closing the progress bar window.")


class ProgressBarClass(tk.Toplevel):

    def __init__(self, parent, addressFile, name, group, typeTest):
        super().__init__(parent)

        self.addressFile = addressFile
        self.name = name
        self.group = group
        self.typeTest = typeTest
        self.window = ""

        # Signals Visualizator Window Configuration
        self.title("SHM Testing")
        self.parent = parent
        self.transient(self.parent)
        self.geometry("400x125+550+250")
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", notClosing)

        # Background Window Wallpaper
        self.image = Image.open("blue_degraded.png")
        self.imageCopy = self.image.copy()

        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg = tk.Label(self, image=self.bgImage)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.bind('<Configure>', self.resizeImage)

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1), weight=1)

        self.labelFile = tk.Label(self, text="SHM is doing the test and creating the datasets", font=("Franklin Gothic Medium", 10), bg='#fcfcf7', borderwidth=3, relief="groove")
        self.labelFile.grid(column=0, row=0, padx=30, pady=15, sticky="NSEW")

        self.progressbar = ttk.Progressbar(self, mode="indeterminate")
        self.progressbar.grid(column=0, row=1, padx=40, pady=15, sticky="NSEW")
        self.progressbar.start()

        if self.parent.valueW == "None":
            self.window = 0
        elif self.parent.valueW == "Hanning":
            self.window = 1
        elif self.parent.valueW == "Hamming":
            self.window = 2
        elif self.parent.valueW == "Flat":
            self.window = 3
        elif self.parent.valueW == "Blackman":
            self.window = 4

        if self.typeTest == "ImpactDetected":
            self.handleImpactDetected()
        elif self.typeTest == "SimpleTest":
            self.handleSimpleTest()
        elif self.typeTest == "PassiveTest":
            self.handlePassiveTest()
        elif self.typeTest == "RoundRobin":
            self.handleRoundRobin()

    def handleSimpleTest(self):
        globals.infoTest = "1 " + self.parent.sampl + " " + self.parent.frec + " " + self.parent.cyc + " " + str(int(self.parent.ampl)/10) + " " + str(self.window) + " " + self.parent.phase + " " + self.parent.initTime + " 0 " + self.parent.valueC[8]

        testThread = AsyncTest(self.addressFile, self.name, self.group, 1, self.parent.valueC[8], self.parent.sampl)
        testThread.start()
        self.monitorThread(testThread)

    def handleRoundRobin(self):
        globals.infoTest = "2 " + self.parent.sampl + " " + self.parent.frec + " " + self.parent.cyc + " " + str(int(self.parent.ampl)/10) + " " + str(self.window) + " " + self.parent.phase + " " + self.parent.initTime + " 0 0"

        testThread = AsyncTest(self.addressFile, self.name, self.group, 2, 0, self.parent.sampl)
        testThread.start()
        self.monitorThread(testThread)

    def handlePassiveTest(self):
        globals.infoTest = "3 " + self.parent.sampl + " 0 0 0 0 0 0 0 0"

        testThread = AsyncTest(self.addressFile, self.name, self.group, 3, 0, self.parent.sampl)
        testThread.start()
        self.monitorThread(testThread)

    def handleImpactDetected(self):
        globals.infoTest = "4 " + self.parent.sampl + " 0 0 0 0 0 0 " + self.parent.th + " 0"

        testThread = AsyncTest(self.addressFile, self.name, self.group, 4, 0, self.parent.sampl)
        testThread.start()
        self.monitorThread(testThread)

    def monitorThread(self, thread):
        if thread.is_alive():
            self.after(250, lambda: self.monitorThread(thread))
        else:
            if globals.testDone:
                tk.messagebox.showinfo("Correct", "Test was donde correctly. Dataset with results created.", parent=self)
                self.destroy()
                self.parent.destroy()
                self.parent.parent.state(newstate="zoomed")
                self.parent.parent.focus_force()
                self.parent.parent.wm_attributes("-disabled", False)
            else:
                self.destroy()
                self.parent.state(newstate="zoomed")
                self.parent.focus_force()
                self.parent.wm_attributes("-disabled", False)

            globals.testDone = False

    def resizeImage(self, event):
        newWidth = event.width
        newHeight = event.height

        self.image = self.imageCopy.resize((newWidth, newHeight))

        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg.configure(image=self.bgImage)

