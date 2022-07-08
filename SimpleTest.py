from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from tkinter_custom_button import TkinterCustomButton
import tkinter as tk
import CreateHDF5, SelectHDF5, ConfigureHDF5
import h5py
import ProgressBar
import globals


class SimpleTest(tk.Toplevel):

    def __init__(self, parent, channel, window):
        super().__init__(parent)

        self.ampl = None
        self.cyc = None
        self.frec = None
        self.addressFile = None
        self.fileSelected = None
        self.phase = None
        self.initTime = None
        self.sampl = None

        self.name = None
        self.address = None

        # Signals Visualizator Window Configuration
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

        self.labelTop = tk.Label(self.frameTop, text='SIMPLE TEST', font=("Arial", 20, "bold", "italic"), bg='#d2e9fa')

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
        self.frameLeft.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        self.labelChannel = tk.Label(self.frameLeft, text="Excitation channel:", font=("Arial", 10), bg='#fcfcf7', borderwidth=0)
        self.labelFrec = tk.Label(self.frameLeft, text="Frequency (Hz):", font=("Arial", 10), bg='#fcfcf7', borderwidth=0)
        self.labelCyc = tk.Label(self.frameLeft, text="Cycles:", font=("Arial", 10), bg='#fcfcf7', borderwidth=0)
        self.labelAmpli = tk.Label(self.frameLeft, text="Amplitude:", font=("Arial", 10), bg='#fcfcf7', borderwidth=0)
        self.labelWindowed = tk.Label(self.frameLeft, text="Type of window:", font=("Arial", 10), bg='#fcfcf7', borderwidth=0)
        self.labelPhase = tk.Label(self.frameLeft, text="Phase:", font=("Arial", 10), bg='#fcfcf7', borderwidth=0)
        self.labelInitTime = tk.Label(self.frameLeft, text="Acquisition start (us):", font=("Arial", 10), bg='#fcfcf7', borderwidth=0)
        self.labelSamples = tk.Label(self.frameLeft, text="Acquisition time (samples):", font=("Arial", 10), bg='#fcfcf7', borderwidth=0)

        self.scrollChannels = tk.Scrollbar(self.frameLeft, orient=tk.VERTICAL)
        self.listboxChannels = tk.Listbox(self.frameLeft, height=2, yscrollcommand=self.scrollChannels.set, exportselection=False)
        self.scrollChannels.configure(command=self.listboxChannels.yview)
        self.listboxChannels.grid(column=2, row=0, padx=5, pady=10, sticky="NSEW")
        self.scrollChannels.grid(column=3, row=0, sticky="NS")
        for i in range(1, 9):
            self.listboxChannels.insert('end', 'Channel %d' % i)

        self.textFrec = tk.Entry(self.frameLeft, font=("Arial", 10), borderwidth=1, relief="solid", width=30)
        self.textFrec.grid(column=2, row=1, ipady=10, padx=10)

        self.textCyc = tk.Entry(self.frameLeft, font=("Arial", 10), borderwidth=1, relief="solid", width=30)
        self.textCyc.grid(column=2, row=2, ipady=10, padx=10)

        self.textAmpli = tk.Entry(self.frameLeft, font=("Arial", 10), borderwidth=1, relief="solid", width=30)
        self.textAmpli.grid(column=2, row=3, ipady=10, padx=10)

        self.scrollWindows = tk.Scrollbar(self.frameLeft, orient=tk.VERTICAL)
        self.listboxWindows = tk.Listbox(self.frameLeft, height=2, yscrollcommand=self.scrollWindows.set, exportselection=False)
        self.scrollWindows.configure(command=self.listboxWindows.yview)
        self.listboxWindows.grid(column=2, row=4, padx=5, pady=10, sticky="NSEW")
        self.scrollWindows.grid(column=3, row=4, sticky="NS")
        self.listboxWindows.insert('end', 'None')
        self.listboxWindows.insert('end', 'Hanning')
        self.listboxWindows.insert('end', 'Hamming')
        self.listboxWindows.insert('end', 'Flat')
        self.listboxWindows.insert('end', 'Blackman')

        self.textPhase = tk.Entry(self.frameLeft, font=("Arial", 10), borderwidth=1, relief="solid", width=30)
        self.textPhase.grid(column=2, row=5, ipady=10, padx=10)

        self.textInitTime = tk.Entry(self.frameLeft, font=("Arial", 10), borderwidth=1, relief="solid", width=30)
        self.textInitTime.grid(column=2, row=6, ipady=10, padx=10)

        self.textSamples = tk.Entry(self.frameLeft, font=("Arial", 10), borderwidth=1, relief="solid", width=30)
        self.textSamples.grid(column=2, row=7, ipady=10, padx=10)

        # FRAME RIGHT
        self.frameRight = tk.Frame(self, borderwidth=3, bg='#fcfcf7', relief="groove")
        self.frameRight.pack(side="right")
        self.frameRight.bind('<Configure>', self.resizeFrameRight)

        # FRAME RIGHT TOP
        self.frameRightTop = tk.LabelFrame(self.frameRight, text="Optional data", bg='#fcfcf7', borderwidth=1)
        self.frameRightTop.columnconfigure((0,1,2,3,4,5), weight=1)
        self.frameRightTop.rowconfigure((0,1,2), weight=1)

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
        self.frameRightMid.columnconfigure((1,2,3), weight=1)
        self.frameRightMid.columnconfigure((0), weight=2)
        self.frameRightMid.rowconfigure((0,1), weight=1)

        self.labelSelectHDF5 = tk.Label(self.frameRightMid, text="Select the HDF5 file and group where the test will be save:", font=("Franklin Gothic Medium", 10), bg='#fcfcf7', borderwidth=0)
        self.textAddress = tk.Text(self.frameRightMid, font=("Franklin Gothic Medium", 9), state=tk.DISABLED, bg='#fcfcf7', width=42, height=2, borderwidth=2)
        self.buttonSelectHDF5 = TkinterCustomButton(master=self.frameRightMid, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=115, height=30, activebg_color="#f5f7d5", text_font=("Century Gothic", 8), text="SELECT", text_color="#17181a", corner_radius=0, command=self.selectHDF5Function)
        self.testName = tk.Label(self.frameRightMid, text="Type a name for the test:", font=("Franklin Gothic Medium", 10), bg='#fcfcf7', borderwidth=0)
        self.textTestName = tk.Entry(self.frameRightMid, borderwidth=1, relief="solid")

        # FRAME RIGHT BUTTON
        self.frameRightButton = tk.Frame(self.frameRight, bg='#fcfcf7', borderwidth=0)
        self.buttonStart = TkinterCustomButton(master=self.frameRightButton, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 12, "bold"), text="START", text_color="#17181a", corner_radius=0, command=self.startTest, width=130)
        self.buttonExit = TkinterCustomButton(master=self.frameRightButton, fg_color='#eb3023', border_color="#1f0404", border_width=2, activebg_color="#e87168", text_font=("Century Gothic", 12, "bold"), text="CANCEL", text_color="white", corner_radius=10, command=self.exitWindow, width=130)

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
        self.labelChannel.grid(column=1, row=0, padx=int(self.winfo_width()*0.01), pady=int(self.winfo_height()*0.035), sticky="E")
        self.labelFrec.grid(column=1, row=1, padx=int(self.winfo_width()*0.01), pady=int(self.winfo_height()*0.035), sticky="E")
        self.labelCyc.grid(column=1, row=2, padx=int(self.winfo_width()*0.01), pady=int(self.winfo_height()*0.035), sticky="E")
        self.labelAmpli.grid(column=1, row=3, padx=int(self.winfo_width()*0.01), pady=int(self.winfo_height()*0.035), sticky="E")
        self.labelWindowed.grid(column=1, row=4, padx=int(self.winfo_width()*0.01), pady=int(self.winfo_height()*0.035), sticky="E")
        self.labelPhase.grid(column=1, row=5, padx=int(self.winfo_width()*0.01), pady=int(self.winfo_height()*0.035), sticky="E")
        self.labelInitTime.grid(column=1, row=6, padx=int(self.winfo_width()*0.01), pady=int(self.winfo_height()*0.035), sticky="E")
        self.labelSamples.grid(column=1, row=7, padx=int(self.winfo_width()*0.01), pady=int(self.winfo_height()*0.035), sticky="E")

        self.labelChannel.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)))
        self.labelFrec.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)))
        self.labelCyc.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)))
        self.labelAmpli.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)))
        self.labelWindowed.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)))
        self.labelPhase.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)))
        self.labelInitTime.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)))
        self.labelSamples.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.007)))

        self.listboxChannels.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))
        self.textFrec.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))
        self.textCyc.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))
        self.textAmpli.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))
        self.listboxWindows.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))
        self.textPhase.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))
        self.textInitTime.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))
        self.textSamples.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))

    def resizeFrameRight(self, event=0):
        self.frameRight.pack(padx=self.winfo_width()*0.03, pady=self.winfo_height()*0.04)

        self.frameRightTop.pack(side="top", padx=self.winfo_width()*0.025, pady=self.winfo_height()*0.015)

        self.addOptionalCheck.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)))
        self.addOptionalCheck.grid(column=0, row=0, columnspan=6, padx=5, pady=10, sticky='EW')
        self.labelUserName.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)))
        self.labelUserName.grid(column=0, row=1, padx=5, pady=10)
        self.textUserName.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))
        self.textUserName.grid(column=1, row=1, ipady=8, padx=5, pady=10)
        self.labelDate.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)))
        self.labelDate.grid(column=2, row=1, padx=5, pady=10)
        self.textDate.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))
        self.textDate.grid(column=3, row=1, ipady=8, padx=10, pady=10)
        self.labelTopology.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)))
        self.labelTopology.grid(column=4, row=1, padx=5, pady=10)
        self.textTopology.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))
        self.textTopology.grid(column=5, row=1, ipady=8, padx=10, pady=10)
        self.labelPiezo.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)))
        self.labelPiezo.grid(column=0, row=2, ipady=8, padx=10, pady=10)
        self.textPiezo.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))
        self.textPiezo.grid(column=1, row=2, ipady=8, padx=10, pady=10)

        self.frameRightMid.pack(side="top", padx=self.winfo_width()*0.025, pady=self.winfo_height()*0.015)
        self.labelSelectHDF5.grid(column=0, row=0, padx=8, pady=10, sticky="w")
        self.textAddress.grid(column=2, row=0, padx=10, pady=10, sticky="ew")
        self.buttonSelectHDF5.grid(column=3, row=0, padx=8, pady=10)
        self.testName.grid(column=0, row=1, padx=8, pady=10, sticky="e")
        self.textTestName.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.007)), width=int(self.winfo_width()*0.015))
        self.textTestName.grid(column=1, row=1, columnspan=3, padx=8, pady=10, ipady=8, sticky="ew")

        self.frameRightButton.pack(side="bottom", padx=self.winfo_width()*0.025, pady=self.winfo_height()*0.015)
        self.buttonExit.pack(side="right", padx=self.winfo_width() * 0.025, pady=self.winfo_height()*0.015)
        self.buttonStart.pack(side="right", padx=self.winfo_width()*0.025, pady=self.winfo_height()*0.015)

    def startTest(self):
        if globals.connected:
            listNotAcceptedLetters = ["'\'", "/", ":", "*", "?", '"', "<", ">", "|"]
            correctName = True

            self.frec = self.textFrec.get()
            self.cyc = self.textCyc.get()
            self.ampl = self.textAmpli.get()
            self.phase = self.textPhase.get()
            self.initTime = self.textInitTime.get()
            self.sampl = self.textSamples.get()

            self.name = self.textTestName.get()
            self.address = self.textAddress.get("1.0", tk.END).strip()

            if not self.frec.isdigit():
                tk.messagebox.showinfo("Frequency error", "Frequency must be a decimal and positive number", parent=self)
                self.focus_force()
            elif not self.cyc.isdigit():
                tk.messagebox.showinfo("Cycles error", "Cycles must be a decimal and positive number", parent=self)
                self.focus_force()
            elif not self.isFloat(self.ampl):
                tk.messagebox.showinfo("Amplitude error", "Amplitude must be a decimal and positive number. To introduce a decimal number use dot instead of comma", parent=self)
                self.focus_force()
            elif not self.phase.isdigit():
                tk.messagebox.showinfo("Phase error", "Phase must be a decimal and positive number", parent=self)
                self.focus_force()
            elif not self.initTime.isdigit():
                tk.messagebox.showinfo("Init time error", "Init time must be a decimal and positive number", parent=self)
                self.focus_force()
            elif not self.sampl.isdigit():
                tk.messagebox.showinfo("Samples error", "Samples must be a natural number", parent=self)
                self.focus_force()
            else:
                if int(self.frec) <= 0:
                    tk.messagebox.showinfo("Frequency error", "Frequency must be bigger than 0", parent=self)
                    self.focus_force()
                elif int(self.cyc) <= 0:
                    tk.messagebox.showinfo("Cycles error", "Cycles must be bigger than 0", parent=self)
                    self.focus_force()
                elif float(self.ampl) < -10 or float(self.ampl) > 10:
                    tk.messagebox.showinfo("Amplitude error", "Amplitude must be between -10 and 10", parent=self)
                    self.focus_force()
                elif int(self.phase) < -360 or int(self.phase) > 360:
                    tk.messagebox.showinfo("Phase error", "Phase must be between -360º and 360º", parent=self)
                    self.focus_force()
                elif int(self.initTime) <= 0:
                    tk.messagebox.showinfo("Init time error", "Init time must be bigger than 0", parent=self)
                    self.focus_force()
                elif int(self.sampl) <= 0:
                    tk.messagebox.showinfo("Samples error", "Samples must be bigger than 0", parent=self)
                    self.focus_force()
                else:

                    # BUSCAR NÚMERO CANAL EN EL TEXTO

                    selection1 = self.listboxChannels.curselection()
                    selection2 = self.listboxWindows.curselection()

                    if not selection1:
                        tk.messagebox.showinfo("Error", 'You must select a channel', parent=self)
                    elif not selection2:
                        tk.messagebox.showinfo("Error", 'You must select a windowed', parent=self)
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
                                tk.messagebox.showinfo("Empty name", 'Type a name for the test. All the files will have a prefix with that name. \nDo not use next characters:  \ / : * ? " < > |', parent=self)
                            else:
                                for i, letter in enumerate(self.address):
                                    if letter == ">":
                                        self.addressFile = self.address[0:i-4]
                                        self.group = self.address[i+4:len(self.address)]

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
                                        dset = grp.create_dataset(self.name + "Params", (8,2), dtype='S30')
                                        dset.attrs['Params'] = True

                                        dset[0, 0] = "Excitation channel"
                                        dset[1, 0] = "Frequency (Hz)"
                                        dset[2, 0] = "Cycles"
                                        dset[3, 0] = "Amplitude"
                                        dset[4, 0] = "Windowed"
                                        dset[5, 0] = "Phase"
                                        dset[6, 0] = "Acquisition start (us)"
                                        dset[7, 0] = "Acquisition time (samples)"

                                        indexC = selection1[0]
                                        self.valueC = self.listboxChannels.get(indexC)

                                        indexW = selection2[0]
                                        self.valueW = self.listboxWindows.get(indexW)

                                        dset[0, 1] = self.valueC
                                        dset[1, 1] = self.frec
                                        dset[2, 1] = self.cyc
                                        dset[3, 1] = self.ampl
                                        dset[4, 1] = self.valueW
                                        dset[5, 1] = self.phase
                                        dset[6, 1] = self.initTime
                                        dset[7, 1] = self.sampl

                                        self.progressBarFunction()

                                    except RuntimeError:
                                        tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)

                                    except ValueError:
                                        tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)
        else:
            tk.messagebox.showinfo("ERROR", "Connection can not be done. Connect a FPGA", parent=self)

    def progressBarFunction(self):
        self.wm_attributes("-disabled", True)
        progressBar = ProgressBar.ProgressBarClass(self, self.addressFile, self.name, self.group, "SimpleTest")
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