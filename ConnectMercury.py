from PIL import Image, ImageTk
import tkinter as tk

from tkinter_custom_button import TkinterCustomButton
from tkinter import messagebox, ttk
from threading import Thread
import globals


class ConnectMercury(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.ip4 = None
        self.ip3 = None
        self.ip2 = None
        self.ip1 = None
        self.parent = parent
        self.transient(self.parent)
        self.minsize(300, 100)
        self.geometry("700x250+400+200")
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.exitWindow)

        # Background Window Wallpaper
        self.image = Image.open("blue_degraded.png")
        self.imageCopy = self.image.copy()
        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg = tk.Label(self, image=self.bgImage)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.bind('<Configure>', self.resizeImage)

        self.lfMercury = tk.LabelFrame(self, text="Connecting with Mercury FPGA", bg='#fcfcf7')
        self.lfMercury.pack(side="top", padx=20, ipadx=200, ipady=60, pady=25)

        self.frameTop = tk.Frame(self.lfMercury, bg='#fcfcf7')
        self.frameTop.pack(side="top", pady=15)
        self.frameTop.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.frameBottom = tk.Frame(self.lfMercury, bg='#fcfcf7')
        self.frameBottom.pack(side="top", pady=15)
        self.frameBottom.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        self.labelMercury = tk.Label(self.frameTop, text="Mercury IP address:", font=("Franklin Gothic Medium", 11), bg='#fcfcf7', borderwidth=0)
        self.textIp1 = tk.Entry(self.frameTop, borderwidth=1, relief="solid", width=10)
        self.textIp1.insert(0, self.parent.ip1)
        self.labelDot1 = tk.Label(self.frameTop, text=".", font=("Franklin Gothic Medium", 15), bg='#fcfcf7', borderwidth=0)
        self.textIp2 = tk.Entry(self.frameTop, borderwidth=1, relief="solid", width=10)
        self.textIp2.insert(0, self.parent.ip2)
        self.labelDot2 = tk.Label(self.frameTop, text=".", font=("Franklin Gothic Medium", 15), bg='#fcfcf7', borderwidth=0)
        self.textIp3 = tk.Entry(self.frameTop, borderwidth=1, relief="solid", width=10)
        self.textIp3.insert(0, self.parent.ip3)
        self.labelDot3 = tk.Label(self.frameTop, text=".", font=("Franklin Gothic Medium", 15), bg='#fcfcf7', borderwidth=0)
        self.textIp4 = tk.Entry(self.frameTop, borderwidth=1, relief="solid", width=10)
        self.textIp4.insert(0, self.parent.ip4)
        self.labelMercury.grid(column=1, row=0, padx=30, pady=10, sticky="NSEW")
        self.textIp1.grid(column=2, row=0, padx=8, ipady=5, pady=10, sticky="EW")
        self.labelDot1.grid(column=3, row=0, pady=10, sticky="EW")
        self.textIp2.grid(column=4, row=0, padx=8, ipady=5, pady=10, sticky="EW")
        self.labelDot2.grid(column=5, row=0, pady=10, sticky="EW")
        self.textIp3.grid(column=6, row=0, padx=8, ipady=5, pady=10, sticky="EW")
        self.labelDot3.grid(column=7, row=0, pady=10, sticky="EW")
        self.textIp4.grid(column=8, row=0, padx=8, ipady=5, pady=10, sticky="EW")

        self.buttonMercury = TkinterCustomButton(master=self.frameBottom, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 9, "bold"), text="CONNECT", text_color="#17181a", corner_radius=0, command=self.connectFunction, width=100, height=35)
        self.buttonDisconnect = TkinterCustomButton(master=self.frameBottom, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 9, "bold"), text="DISCONNECT", text_color="#17181a", corner_radius=0, command=self.disconnectFunction, width=100, height=35)
        self.buttonCancel = TkinterCustomButton(master=self.frameBottom, fg_color='#eb3023', border_color="#1f0404", border_width=2, activebg_color="#e87168", text_font=("Century Gothic", 9, "bold"), text="CANCEL", text_color="white", corner_radius=10, command=self.exitWindow, width=100, height=35)
        self.buttonMercury.grid(column=2, row=0, padx=25)
        self.buttonDisconnect.grid(column=3, row=0, padx=25)
        self.buttonCancel.grid(column=4, row=0, padx=25)

    def disconnectFunction(self):
        if globals.connected:
            globals.threadComm = "exit"
            tk.messagebox.showinfo("Disconnect Mercury", "Disconnecting FPGA Mercury.", parent=self)
        else:
            tk.messagebox.showinfo("Error", "There is not FPGA Mercury connected.", parent=self)

    def connectFunction(self):
        self.ip1 = self.parent.ip1 = self.textIp1.get()
        self.ip2 = self.parent.ip2 = self.textIp2.get()
        self.ip3 = self.parent.ip3 = self.textIp3.get()
        self.ip4 = self.parent.ip4 = self.textIp4.get()

        if not self.ip1.isdigit() or not self.ip2.isdigit() or not self.ip3.isdigit() or not self.ip4.isdigit():
            tk.messagebox.showinfo("Ip error", "Address must be a natural and positive number", parent=self)
            self.focus_force()
        elif int(self.ip1) > 255 or int(self.ip2) > 255 or int(self.ip3) > 255 or int(self.ip4) > 255:
            tk.messagebox.showinfo("Ip error", "Number can not be bigger than 255", parent=self)
            self.focus_force()
        else:
            globals.HOST = self.ip1 + "." + self.ip2 + "." + self.ip3 + "." + self.ip4

            self.wm_attributes("-disabled", True)
            progressBar = ProgressBarConnectMercury(self, globals.HOST)
            progressBar.focus_force()

    def exitWindow(self):
        self.destroy()
        self.parent.state(newstate="zoomed")
        self.parent.focus_force()
        self.parent.wm_attributes("-disabled", False)

    def resizeImage(self, event):
        newWidth = event.width
        newHeight = event.height

        self.image = self.imageCopy.resize((newWidth, newHeight))

        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg.configure(image=self.bgImage)


class ProgressBarConnectMercury(tk.Toplevel):

    def __init__(self, parent, HOST):
        super().__init__(parent)

        # Signals Visualizator Window Configuration
        self.title("SHM Connecting with Mercury")
        self.parent = parent
        self.transient(self.parent)
        self.geometry("400x125+550+250")
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.notClosing)

        # Background Window Wallpaper
        self.image = Image.open("blue_degraded.png")
        self.imageCopy = self.image.copy()

        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg = tk.Label(self, image=self.bgImage)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.bind('<Configure>', self.resizeImage)

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1), weight=1)

        self.labelFile = tk.Label(self, text="Software is connecting with Mercury FPGA",
                                  font=("Franklin Gothic Medium", 10), bg='#fcfcf7', borderwidth=3, relief="groove")
        self.labelFile.grid(column=0, row=0, padx=30, pady=15, sticky="NSEW")

        self.progressbar = ttk.Progressbar(self, mode="indeterminate")
        self.progressbar.grid(column=0, row=1, padx=40, pady=15, sticky="NSEW")
        self.progressbar.start()

        testThread = AsyncTest(HOST)
        testThread.start()
        self.monitorThread(testThread)

    def monitorThread(self, thread):
        if thread.is_alive():
            self.after(250, lambda: self.monitorThread(thread))
        else:
            self.destroy()
            self.parent.wm_attributes("-disabled", False)
            self.parent.focus_force()

            if not globals.connected:
                tk.messagebox.showinfo("Connection error", "Connection failed: Init python file in mercury FPGA or change ip address.", parent=self.parent)
            else:
                tk.messagebox.showinfo("Connection done", "Connection was done correctly.", parent=self.parent)
                self.parent.destroy()
                self.parent.parent.state(newstate="zoomed")
                self.parent.parent.focus_force()
                self.parent.parent.wm_attributes("-disabled", False)

    def resizeImage(self, event):
        newWidth = event.width
        newHeight = event.height

        self.image = self.imageCopy.resize((newWidth, newHeight))

        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg.configure(image=self.bgImage)

    def notClosing(self):
        print("By doing this the user can not cancel de process and closing the progress bar window.")


class AsyncTest(Thread):
    def __init__(self, HOST):
        super().__init__()

        self.PORT = 65432  # The port used by the server

    def run(self):
        try:
            print("Intenta conexión")
            globals.sock.connect((globals.HOST, self.PORT))
            print("Se conecta")
            globals.connected = True
            globals.threadComm = "connect"
        except:
            globals.connected = False
