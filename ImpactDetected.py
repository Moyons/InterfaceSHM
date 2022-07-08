from PIL import Image, ImageTk
from tkinter import ttk, messagebox

import ProgressBar
from tkinter_custom_button import TkinterCustomButton
from tkinter import filedialog
import tkinter as tk
import globals
import h5py
import SelectHDF5

class ImpactDetected(tk.Toplevel):

    def __init__(self, parent, channel, window):
        super().__init__(parent)

        # Signals Visualizator Window Configuration
        self.address = None
        self.name = None
        self.th = None
        self.sampl = None
        self.parent = parent
        self.channel = channel
        self.window = window
        self.minsize(1100, 675)
        self.state('zoomed')

        self.protocol("WM_DELETE_WINDOW", self.exitWindow)

        # Background Window Wallpaper
        self.image = Image.open("blue_degraded.png")
        self.imageCopy = self.image.copy()

        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg = tk.Label(self, image=self.bgImage)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.bind('<Configure>', self.resizeImage)

        # FRAME TOP
        self.frameTop = tk.Frame(self, bg='#d2e9fa', borderwidth=3, relief="groove")
        self.frameTop.pack(side="top", fill="x")
        self.frameTop.bind('<Configure>', self.resizeFrameTop)

        self.labelTop = tk.Label(self.frameTop, text='IMPACT DETECTED', font=("Arial", 20, "bold", "italic"), bg='#d2e9fa')

        self.imageISATI = Image.open("ISATIlogo.jpg")
        self.imageISATI.thumbnail((120,50))
        self.imageISATI = ImageTk.PhotoImage(self.imageISATI)
        self.labelISATI = tk.Label(self.frameTop, image=self.imageISATI, bg='#d2e9fa')

        # FRAME LEFT
        self.frameLeft = tk.Frame(self, bg='#fcfcf7', borderwidth=3, relief="groove")
        self.frameLeft.pack(side="left")
        self.frameLeft.bind('<Configure>', self.resizeFrameLeft)

        self.frameLeft.columnconfigure((0, 2, 3), weight=1)
        self.frameLeft.columnconfigure(1, weight=2)
        self.frameLeft.rowconfigure((0, 1), weight=1)

        self.labelSamples = tk.Label(self.frameLeft, text="Acquisition time (samples):", font=("Arial", 10), bg='#fcfcf7', borderwidth=0)
        self.labelTreshold = tk.Label(self.frameLeft, text="Threshold:", font=("Arial", 10), bg='#fcfcf7', borderwidth=0)

        self.textSamples = tk.Entry(self.frameLeft, font=("Arial", 10), borderwidth=1, relief="solid", width=30)
        self.textSamples.grid(column=2, row=0, ipady=10, padx=10)

        self.textTreshold = tk.Entry(self.frameLeft, font=("Arial", 10), borderwidth=1, relief="solid", width=30)
        self.textTreshold.grid(column=2, row=1, ipady=10, padx=10)

        # FRAME RIGHT
        self.frameRight = tk.Frame(self, borderwidth=3, bg='#fcfcf7', relief="groove")
        self.frameRight.pack(side="right")
        self.frameRight.bind('<Configure>', self.resizeFrameRight)

        # FRAME RIGHT TOP
        self.frameRightTop = tk.LabelFrame(self.frameRight, text="Optional data", bg='#fcfcf7', borderwidth=1)
        self.frameRightTop.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.frameRightTop.rowconfigure((0, 1, 2), weight=1)

        self.addOpt = tk.IntVar()
        self.addOptionalCheck = tk.Checkbutton(self.frameRightTop, text="Adding optional data", variable=self.addOpt, onvalue=1, offvalue=0)
        self.labelUserName = tk.Label(self.frameRightTop, text="User name:", bg='#fcfcf7', borderwidth=0)
        self.textUserName = tk.Entry(self.frameRightTop, borderwidth=1, relief="solid", width=20)
        self.labelDate = tk.Label(self.frameRightTop, text="Date:", bg='#fcfcf7', borderwidth=0)
        self.textDate = tk.Entry(self.frameRightTop, borderwidth=1, relief="solid", width=20)
        self.labelTopology = tk.Label(self.frameRightTop, text="Topology:", bg='#fcfcf7', borderwidth=0)
        self.textTopology = tk.Entry(self.frameRightTop, borderwidth=1, relief="solid", width=20)
        self.labelPiezo = tk.Label(self.frameRightTop, text="Piezoelectric:", bg='#fcfcf7', borderwidth=0)
        self.textPiezo = tk.Entry(self.frameRightTop, borderwidth=1, relief="solid", width=20)

        # FRAME RIGHT MID
        self.frameRightMid = tk.LabelFrame(self.frameRight, text="HDF5 file", bg='#fcfcf7', borderwidth=1)
        self.frameRightMid.columnconfigure((1, 2, 3), weight=1)
        self.frameRightMid.columnconfigure((0), weight=2)
        self.frameRightMid.rowconfigure((0, 1), weight=1)

        self.labelSelectHDF5 = tk.Label(self.frameRightMid, text="Select the HDF5 file and group where the test will be save:", font=("Franklin Gothic Medium", 10), bg='#fcfcf7', borderwidth=0)
        self.textAddress = tk.Text(self.frameRightMid, font=("Franklin Gothic Medium", 9), state=tk.DISABLED, bg='#fcfcf7', width=42, height=2, borderwidth=2)
        self.buttonSelectHDF5 = TkinterCustomButton(master=self.frameRightMid, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=115, height=30, activebg_color="#f5f7d5", text_font=("Century Gothic", 8), text="SELECT", text_color="#17181a", corner_radius=0, command=self.selectHDF5Function)
        self.testName = tk.Label(self.frameRightMid, text="Type a name for the test:", font=("Franklin Gothic Medium", 10), bg='#fcfcf7', borderwidth=0)
        self.textTestName = tk.Entry(self.frameRightMid, borderwidth=1, relief="solid")

        # FRAME RIGHT BUTTON
        self.frameRightButton = tk.Frame(self.frameRight, bg='#fcfcf7', borderwidth=0)
        self.buttonStart = TkinterCustomButton(master=self.frameRightButton, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 12, "bold"), text="START", text_color="#17181a", corner_radius=0, command=self.startTest, width=130)
        self.buttonExit = TkinterCustomButton(master=self.frameRightButton,fg_color='#eb3023', border_color="#1f0404", border_width=2, activebg_color="#e87168", text_font=("Century Gothic", 12, "bold"), text="CANCEL", text_color="white", corner_radius=10, command=self.exitWindow, width=130)

    def resizeImage(self, event):
        newWidth = event.width
        newHeight = event.height

        self.image = self.imageCopy.resize((newWidth, newHeight))

        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg.configure(image=self.bgImage)


    def resizeFrameTop(self, event=0):
        self.labelTop.pack(side="left", padx=self.winfo_width()*0.035, pady=self.winfo_height()*0.02)
        self.labelISATI.pack(side="right", padx=self.winfo_width()*0.035)


    def resizeFrameLeft(self, event=0):
        self.frameLeft.pack(padx=self.winfo_width()*0.03, pady=self.winfo_height()*0.04)

        # Ajustar aquí el pady y el padx directamente
        self.labelSamples.grid(column=1, row=0, padx=int(self.winfo_width()*0.01), pady=int(self.winfo_height()*0.035), sticky="E")
        self.labelTreshold.grid(column=1, row=1, padx=int(self.winfo_width() * 0.01), pady=int(self.winfo_height() * 0.035), sticky="E")

        self.labelSamples.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)))
        self.labelTreshold.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)))

        self.textSamples.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))
        self.textTreshold.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))

    def resizeFrameRight(self, event=0):
        self.frameRight.pack(padx=self.winfo_width() * 0.03, pady=self.winfo_height() * 0.04)

        self.frameRightTop.pack(side="top", padx=self.winfo_width() * 0.025, pady=self.winfo_height() * 0.015)

        self.addOptionalCheck.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)))
        self.addOptionalCheck.grid(column=0, row=0, columnspan=6, padx=5, pady=10, sticky='EW')
        self.labelUserName.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)))
        self.labelUserName.grid(column=0, row=1, padx=5, pady=10)
        self.textUserName.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)), width=int(self.winfo_width() * 0.015))
        self.textUserName.grid(column=1, row=1, ipady=8, padx=5, pady=10)
        self.labelDate.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)))
        self.labelDate.grid(column=2, row=1, padx=5, pady=10)
        self.textDate.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)), width=int(self.winfo_width() * 0.015))
        self.textDate.grid(column=3, row=1, ipady=8, padx=10, pady=10)
        self.labelTopology.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)))
        self.labelTopology.grid(column=4, row=1, padx=5, pady=10)
        self.textTopology.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)), width=int(self.winfo_width() * 0.015))
        self.textTopology.grid(column=5, row=1, ipady=8, padx=10, pady=10)
        self.labelPiezo.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)))
        self.labelPiezo.grid(column=0, row=2, ipady=8, padx=10, pady=10)
        self.textPiezo.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)), width=int(self.winfo_width() * 0.015))
        self.textPiezo.grid(column=1, row=2, ipady=8, padx=10, pady=10)

        self.frameRightMid.pack(side="top", padx=self.winfo_width() * 0.025, pady=self.winfo_height() * 0.015)
        self.labelSelectHDF5.grid(column=0, row=0, padx=8, pady=10, sticky="w")
        self.textAddress.grid(column=2, row=0, padx=10, pady=10, sticky="ew")
        self.buttonSelectHDF5.grid(column=3, row=0, padx=8, pady=10)
        self.testName.grid(column=0, row=1, padx=8, pady=10, sticky="e")
        self.textTestName.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)), width=int(self.winfo_width() * 0.015))
        self.textTestName.grid(column=1, row=1, columnspan=3, padx=8, pady=10, ipady=8, sticky="ew")

        self.frameRightButton.pack(side="bottom", padx=self.winfo_width() * 0.025, pady=self.winfo_height() * 0.015)
        self.buttonExit.pack(side="right", padx=self.winfo_width() * 0.025, pady=self.winfo_height() * 0.015)
        self.buttonStart.pack(side="right", padx=self.winfo_width() * 0.025, pady=self.winfo_height() * 0.015)

    def startTest(self):
        if globals.connected:
            listNotAcceptedLetters = ["'\'", "/", ":", "*", "?", '"', "<", ">", "|"]
            correctName = True

            self.sampl = self.textSamples.get()
            self.th = self.textTreshold.get()

            self.name = self.textTestName.get()
            self.address = self.textAddress.get("1.0", tk.END).strip()

            if not self.sampl.isdigit():
                tk.messagebox.showinfo("Samples error", "Samples must be a natural number", parent=self)
                self.focus_force()
            elif not self.th.isdigit():
                tk.messagebox.showinfo("Treshold error", "Treshold must be a natural number", parent=self)
                self.focus_force()
            else:
                if int(self.sampl) <= 0:
                    tk.messagebox.showinfo("Samples error", "Samples must be bigger than 0", parent=self)
                    self.focus_force()
                elif int(self.th) <= 0:
                    tk.messagebox.showinfo("Treshold error", "Treshold must be bigger than 0", parent=self)
                    self.focus_force()
                else:
                    if not self.address:
                        tk.messagebox.showinfo("Empty address", 'Select a file and a group where the files will be saved', parent=self)
                    else:
                        for letter in self.name:
                            for notAccepted in listNotAcceptedLetters:
                                if letter == notAccepted:
                                    correctName = False
                                    break

                        if not self.name or not correctName:
                            tk.messagebox.showinfo("Empty name", 'Type a name for the test. All the files will have a prefix with that name.\nDo not use next characters:  \ / : * ? " < > |', parent=self)
                        else:
                            for i, letter in enumerate(self.address):
                                if letter == ">":
                                    self.addressFile = self.address[0:i - 4]
                                    self.group = self.address[i + 4:len(self.address)]

                            if self.addOpt.get():
                                with h5py.File(self.addressFile, "a") as f:
                                    try:
                                        grp = f.require_group(self.group)
                                        dset = grp.create_dataset(self.name + "Extras", (4, 2), dtype='S50')
                                        dset.attrs['Extras'] = True

                                        dset[0, 0] = "User Name"
                                        dset[1, 0] = "Date"
                                        dset[2, 0] = "Topology"
                                        dset[3, 0] = "Piezoelectric"

                                        dset[0, 1] = self.textUserName.get()
                                        dset[1, 1] = self.textDate.get()
                                        dset[2, 1] = self.textTopology.get()
                                        dset[3, 1] = self.textPiezo.get()

                                    except RuntimeError:
                                        tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)

                                    except ValueError:
                                        tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)

                            with h5py.File(self.addressFile, "a") as f:
                                try:
                                    grp = f.require_group(self.group)
                                    dset = grp.create_dataset(self.name + "Params", (2, 2), dtype='S30')
                                    dset.attrs['Params'] = True

                                    dset[0, 0] = "Acquisition time (samples)"
                                    dset[1, 0] = "Treshold"

                                    dset[0, 1] = self.sampl
                                    dset[1, 1] = self.th

                                    self.progressBarFunction()

                                except RuntimeError:
                                    tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)

                                except ValueError:
                                    tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)
        else:
            tk.messagebox.showinfo("ERROR", "Connection can not be done. Connect a FPGA", parent=self)

    def progressBarFunction(self):
        self.wm_attributes("-disabled", True)
        progressBar = ProgressBar.ProgressBarClass(self, self.addressFile, self.name, self.group, "ImpactDetected")
        progressBar.focus_force()

    def selectHDF5Function(self):
        self.wm_attributes("-disabled", True)
        selectHDF5 = SelectHDF5.SelectHDF5(self)
        selectHDF5.focus_force()

    def exitWindow(self):
        self.destroy()
        self.parent.state(newstate="zoomed")
        self.parent.focus_force()

    def isFloat(self, elemento):
        try:
            float(elemento)
            return True
        except ValueError:
            return False