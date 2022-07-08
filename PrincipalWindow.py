import time
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

from threading import Thread
import ConfigureHDF5, ConnectMercury
import SignalsVisualizator, SimpleTest, RoundRobin, PassiveTest, ImpactDetected, CreateHDF5
import globals
from tkinter_custom_button import TkinterCustomButton


class Aplication(tk.Tk):

    def __init__(self):
        super().__init__()

        # Principal Window Configuration
        self.title("SHM Software")
        self.minsize(1100, 700)
        self.state('zoomed')
        self.protocol("WM_DELETE_WINDOW", self.exitFunction)

        self.ip1 = ""
        self.ip2 = ""
        self.ip3 = ""
        self.ip4 = ""

        # Background Window Wallpaper
        self.image = Image.open("blue_degraded.png")
        self.imageCopy = self.image.copy()

        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg = tk.Label(self, image=self.bgImage)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.bind('<Configure>', self.resizeImage)

        # PRINCIPAL WINDOW LAYOUT
        # FRAME TOP
        self.frameTop = tk.Frame(self, bg='#d2e9fa', borderwidth=3, relief="groove")
        self.frameTop.pack(side="top", fill="x")
        self.frameTop.bind('<Configure>', self.resizeFrameTop)

        self.labelTop = tk.Label(self.frameTop, text='SHM Software', font=("Arial", 27, "bold", "italic"), bg='#d2e9fa')

        self.imageISATI = Image.open("ISATIlogo.jpg")
        self.imageISATI.thumbnail((140, 60))
        self.imageISATI = ImageTk.PhotoImage(self.imageISATI)
        self.labelISATI = tk.Label(self.frameTop, image=self.imageISATI, bg='#d2e9fa')

        self.imageUPM = Image.open("UPMlogo.png")
        self.imageUPM.thumbnail((140, 60))
        self.imageUPM = ImageTk.PhotoImage(self.imageUPM)
        self.labelUPM = tk.Label(self.frameTop, image=self.imageUPM, bg='#d2e9fa')

        # FRAME CENTER
        self.frameCenter = tk.Frame(self, bg='#fcfcf7', borderwidth=4, relief="groove")
        self.frameCenter.pack(expand=1)
        self.frameCenter.bind('<Configure>', self.resizeFrameCenter)

        self.frameCenter1 = tk.Frame(self.frameCenter, bg='#fcfcf7')
        self.frameCenter1.pack(side="top")
        self.frameCenter2 = tk.Frame(self.frameCenter, bg='#fcfcf7')
        self.frameCenter2.pack(side="top")
        self.frameCenter2.columnconfigure((0, 1, 2, 3), weight=1)
        self.frameCenter2.rowconfigure((0, 1), weight=1)
        self.frameCenter3 = tk.Frame(self.frameCenter, bg='#fcfcf7')
        self.frameCenter3.pack(side="top")
        self.frameCenter4 = tk.Frame(self.frameCenter, bg='#fcfcf7')
        self.frameCenter4.pack(side="top")
        self.frameCenter5 = tk.Frame(self.frameCenter, bg='#fcfcf7')
        self.frameCenter5.pack(side="top")
        self.frameCenter5.columnconfigure((0, 1, 2, 3), weight=1)
        self.frameCenter5.rowconfigure((0, 1), weight=1)
        self.frameCenter6 = tk.Frame(self.frameCenter, bg='#fcfcf7')
        self.frameCenter6.pack(side="top")

        # FRAME CENTER 1
        self.labelFC1 = tk.Label(self.frameCenter1, text='CONFIGURING HDF5 FILES', font=("Franklin Gothic Medium", 13, "bold", "underline"), fg='black', bg='#fcfcf7')
        self.textFC1 = "In this section the user can create a new HDF5 file or configure the groups and datasets in several HDF5 files."  # Igual hay que aumentar este texto explicando mas
        self.labelTextFC1 = tk.Label(self.frameCenter1, text=self.textFC1, font=("Franklin Gothic Medium", 11), fg='black', bg='#fcfcf7')

        # FRAME CENTER 2
        self.botonFC2a = TkinterCustomButton(master=self.frameCenter2, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 11, "bold"), text="CREATE HDF5", text_color="#17181a", corner_radius=0, command=self.createHDF5Function, height=35)
        self.botonFC2b = TkinterCustomButton(master=self.frameCenter2, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 11, "bold"), text="CONFIGURE HDF5", text_color="#17181a", corner_radius=0, command=self.configureHDF5Function, height=35, width=150)

        self.canvas1 = tk.Canvas(self.frameCenter2, bg='#737370')

        # FRAME CENTER 3
        self.labelFC3 = tk.Label(self.frameCenter3, text='SET UP A TEST', font=("Franklin Gothic Medium", 13, "bold", "underline"), fg='black', bg='#fcfcf7')
        self.textFC3 = "In this section the user can select a test from the ones below. The user will have to parameterize the selected test."  # Igual hay que aumentar este texto explicando mas
        self.labelTextFC3 = tk.Label(self.frameCenter3, text=self.textFC3, font=("Franklin Gothic Medium", 11), fg='black', bg='#fcfcf7')

        # FRAME CENTER 4
        self.botonST = TkinterCustomButton(master=self.frameCenter4, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 11, "bold"), text="SIMPLE TEST", text_color="#17181a", corner_radius=0, command=self.simpleTestFunction, height=35)
        self.botonRR = TkinterCustomButton(master=self.frameCenter4, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5",  text_font=("Century Gothic", 11, "bold"), text="ROUND ROBIN", text_color="#17181a", corner_radius=0, command=self.roundRobinFunction, height=35)
        self.botonPT = TkinterCustomButton(master=self.frameCenter4, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 11, "bold"), text="PASSIVE TEST", text_color="#17181a", corner_radius=0, command=self.passiveTestFunction, height=35)
        self.botonID = TkinterCustomButton(master=self.frameCenter4, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 11, "bold"), text="IMPACT DETECTED", text_color="#17181a", corner_radius=0, command=self.impactDetectedFunction, height=35, width=150)

        self.canvas2 = tk.Canvas(self.frameCenter4, bg='#737370')

        # FRAME CENTER 5
        self.labelFC5 = tk.Label(self.frameCenter5, text='OPEN HDF5 FILES', fg='black', bg='#fcfcf7')
        self.textFC5 = "In this section the user can open one or several (up to three) HDF5 files and visualize them. The user will also be able to test \nsome algorithms with the selected signals and save them."
        self.labelTextFC5 = tk.Label(self.frameCenter5, text=self.textFC5, fg='black', bg='#fcfcf7')
        self.botonVis = TkinterCustomButton(master=self.frameCenter5, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 11, "bold"), text="VISUALIZE", text_color="#17181a", corner_radius=0, command=self.visualizeFunction, height=35)

        # FRAME CENTER 6
        self.labelFC6 = tk.Label(self.frameCenter6, bg='#fcfcf7')
        self.botonConnect = TkinterCustomButton(master=self.frameCenter6, fg_color='#969692', border_color="#1f0404", border_width=2, activebg_color="#d1d1cb", text_font=("Century Gothic", 10, "bold"), text="CONNECT MERCURY", text_color="white", corner_radius=10, height=35, width=160, command=self.connectMercury)
        self.botonExit = TkinterCustomButton(master=self.frameCenter6, fg_color='#eb3023', border_color="#1f0404", border_width=2, activebg_color="#e87168",text_font=("Century Gothic", 11, "bold"), text="EXIT", text_color="white", corner_radius=10, height=35, command=self.exitFunction)

    def resizeImage(self, event):
        newWidth = event.width
        newHeight = event.height

        self.image = self.imageCopy.resize((newWidth, newHeight))

        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg.configure(image=self.bgImage)

    def resizeFrameTop(self, event=0):
        self.labelTop.pack(side="left", padx=self.winfo_width()*0.035, pady=self.winfo_height()*0.03)
        self.labelUPM.pack(side="right", padx=self.winfo_width()*0.02)
        self.labelISATI.pack(side="right")

    def resizeFrameCenter(self, event=0):
        self.labelFC1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.01), "bold", "underline"))
        self.labelFC1.pack(side="top", padx=self.winfo_width()*0.3, pady=self.winfo_height()*0.02)
        self.labelTextFC1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0075)))
        self.labelTextFC1.pack(side="top")

        self.botonFC2a.grid(column=1, row=0, pady=self.winfo_height()*0.02)
        self.botonFC2b.grid(column=2, row=0, pady=self.winfo_height() * 0.02)
        self.canvas1.config(width=self.winfo_width()*0.65, height=self.winfo_height()*0.002)
        self.canvas1.grid(column=0, row=1, columnspan=4, pady=self.winfo_height() * 0.02)

        self.labelFC3.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.01), "bold", "underline"))
        self.labelFC3.pack(side="top", padx=self.winfo_width()*0.3, pady=self.winfo_height()*0.02)
        self.labelTextFC3.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0075)))
        self.labelTextFC3.pack(side="top")

        self.botonST.grid(column=0, row=0, pady=self.winfo_height()*0.02)
        self.botonRR.grid(column=1, row=0, pady=self.winfo_height()*0.02)
        self.botonPT.grid(column=2, row=0, pady=self.winfo_height()*0.02)
        self.botonID.grid(column=3, row=0, pady=self.winfo_height()*0.02)

        self.canvas2.config(width=self.winfo_width()*0.65, height=self.winfo_height()*0.002)
        self.canvas2.grid(column=0, row=1, columnspan=4, pady=self.winfo_height()*0.02)

        self.labelFC5.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.01), "bold", "underline"))
        self.labelFC5.pack(side="top", pady=self.winfo_height()*0.015)
        self.labelTextFC5.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0075)))
        self.labelTextFC5.pack(side="top")
        self.botonVis.pack(side="left", pady=self.winfo_height()*0.01, expand=True)

        self.labelFC6.pack(side="top", padx=self.winfo_width()*0.35)
        self.botonConnect.pack(side="left", pady=self.winfo_height()*0.01)
        self.botonExit.pack(side="right", pady=self.winfo_height()*0.01)

    def exitFunction(self):
        result = tk.messagebox.askyesno("Exit", "Are you sure you want to exit the app?", parent=self)
        if result:
            globals.threadComm = "exit"
            self.destroy()
            print("Adios principal")

    def createHDF5Function(self):
        self.wm_attributes("-disabled", True)
        createHDF5 = CreateHDF5.CreateHDF5(self)
        createHDF5.focus_force()

    def connectMercury(self):
        self.wm_attributes("-disabled", True)
        connectMercury = ConnectMercury.ConnectMercury(self)
        connectMercury.focus_force()

    def configureHDF5Function(self):
        configureHDF5 = ConfigureHDF5.ConfigureHDF5(self)
        configureHDF5.focus_force()
        self.state(newstate="withdraw")

    def visualizeFunction(self):
        nuevaVentana = SignalsVisualizator.SignalsVisualizator(self)
        nuevaVentana.focus_force()
        self.state(newstate="withdraw")

    def simpleTestFunction(self):
        simpleTest = SimpleTest.SimpleTest(self, "", "")
        simpleTest.focus_force()
        self.state(newstate="withdraw")

    def roundRobinFunction(self):
        roundRobin = RoundRobin.RoundRobin(self, "", "")
        roundRobin.focus_force()
        self.state(newstate="withdraw")

    def passiveTestFunction(self):
        passiveTest = PassiveTest.PassiveTest(self, "", "")
        passiveTest.focus_force()
        self.state(newstate="withdraw")

    def impactDetectedFunction(self):
        impactDetected = ImpactDetected.ImpactDetected(self, "", "")
        impactDetected.focus_force()
        self.state(newstate="withdraw")


def softwareSHM():
    app = Aplication()
    app.mainloop()


def controlMercury():
    while True:
        time.sleep(0.25)
        try:
            if globals.threadComm == "exit":
                if globals.connected:
                    print("Se desconecta de la FPGA conectada")
                    message = "EXIT"
                    globals.sock.send(message.encode())
                    globals.sock.recv(1024)
                    globals.sock.close()
                    globals.initialize()
                    break
                else:
                    print("Se mata el hilo")
                    break
            elif globals.threadComm == "connect":
                message = "Connected"
                globals.sock.send(message.encode())
                globals.sock.recv(1024)
            elif globals.threadComm == "test":
                print("Enviamos que queremos empezar un test")
                message = globals.infoTest
                globals.sock.send(message.encode())
                print("Esperamos a que nos devuelva el resultado de que ha acabado el test")
                result = globals.sock.recv(1024)
                if result.decode() == "Finish":
                    globals.testDone = True
                    globals.threadComm = "connect"
        except ConnectionResetError:
            globals.connected = False
            pass


if __name__ == '__main__':
    globals.initialize()

    aplication = Aplication()
    Thread(target=controlMercury).start()
    # Thread(target=softwareSHM).start()

    aplication.mainloop()


