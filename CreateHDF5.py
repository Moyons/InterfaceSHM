from PIL import Image, ImageTk
import tkinter as tk
import h5py
from tkinter_custom_button import TkinterCustomButton
from tkinter import filedialog, messagebox


class CreateHDF5(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.transient(self.parent)
        self.minsize(300, 100)
        self.geometry("750x300+412+200")
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.exitWindow)

        # Background Window Wallpaper
        self.image = Image.open("blue_degraded.png")
        self.imageCopy = self.image.copy()
        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg = tk.Label(self, image=self.bgImage)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.bind('<Configure>', self.resizeImage)

        self.lfCreateHDF5 = tk.LabelFrame(self, text="Creating a HDF5 file", bg='#fcfcf7')
        self.lfCreateHDF5.pack(side="top", padx=20, ipadx=200, ipady=60, pady=25)

        self.lfCreateHDF5.columnconfigure((0,1,2,3,4,5), weight=1)
        self.lfCreateHDF5.rowconfigure((0,1,2,3), weight=1)

        self.labelFileName = tk.Label(self.lfCreateHDF5, text="File name:", font=("Franklin Gothic Medium", 11), bg='#fcfcf7', borderwidth=0)
        self.textFileName = tk.Entry(self.lfCreateHDF5, borderwidth=1, relief="solid")
        self.labelFileName.grid(column=1, row=0, padx=30, pady=10, sticky="NSEW")
        self.textFileName.grid(column=2, row=0, ipady=5, pady=10, sticky="EW", columnspan=3)

        self.labelDirectory = tk.Label(self.lfCreateHDF5, text="Directory:", font=("Franklin Gothic Medium", 11), bg='#fcfcf7', borderwidth=0)
        self.labelDirectory.grid(column=1, row=1, padx=30, sticky="NSEW")
        self.textAddress = tk.Text(self.lfCreateHDF5, font=("Franklin Gothic Medium",8), state=tk.DISABLED, bg='#fcfcf7', width=75, height=2)
        self.textAddress.grid(column=2, row=1, columnspan=2)
        self.buttonDirectory = TkinterCustomButton(master=self.lfCreateHDF5, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=85, height=25, activebg_color="#f5f7d5", text_font=("Century Gothic", 7), text="Select Directory", text_color="#17181a", corner_radius=0, command=self.openDirectoryFunction)
        self.buttonDirectory.grid(column=5, row=1, padx=20)

        self.buttonCreateHDF5 = TkinterCustomButton(master=self.lfCreateHDF5, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 10, "bold"), text="CREATE", text_color="#17181a", corner_radius=0, command=self.createFunction, width=125)
        self.buttonCancel = TkinterCustomButton(master=self.lfCreateHDF5, fg_color='#eb3023', border_color="#1f0404", border_width=2, activebg_color="#e87168", text_font=("Century Gothic", 10, "bold"), text="CANCEL", text_color="white", corner_radius=10, command=self.exitWindow, width=125)
        self.buttonCreateHDF5.grid(column=2, row=3)
        self.buttonCancel.grid(column=3, row=3)

    def createFunction(self):

        self.correctName = True
        self.listNotAcceptedLetters = ["'\'", "/", ":", "*", "?", '"', "<", ">", "|"]
        self.name = self.textFileName.get()
        self.address = self.textAddress.get("1.0", tk.END).strip()
        if not self.address: #strip is used strip white spaces
            tk.messagebox.showinfo("Empty directory", 'There is no directory selected', parent=self)
        else:
            for letter in self.name:
                for notAccepted in self.listNotAcceptedLetters:
                    if letter == notAccepted:
                        self.correctName = False
                        break

            if self.correctName and self.name:
                self.completeAddress = self.address + "/" + self.name + ".hdf5"
                self.newHDF5File = h5py.File(self.completeAddress, "w")
                self.newHDF5File.close()

                self.destroy()
                self.parent.state(newstate="zoomed")
                self.parent.focus_force()
                self.parent.wm_attributes("-disabled", False)
            else:
                tk.messagebox.showinfo("Incorrect name", 'File name must have characters except: \ / : * ? " < > | ', parent=self)


    def exitWindow(self):
        self.destroy()
        self.parent.state(newstate="zoomed")
        self.parent.focus_force()
        self.parent.wm_attributes("-disabled", False)

    def openDirectoryFunction(self):
        folder = filedialog.askdirectory()
        self.textAddress.config(state=tk.NORMAL)
        self.textAddress.delete('1.0', tk.END)
        self.textAddress.insert('1.0', folder)
        self.textAddress.config(state=tk.DISABLED)
        self.focus_force()

    def resizeImage(self, event):
        newWidth = event.width
        newHeight = event.height

        self.image = self.imageCopy.resize((newWidth, newHeight))

        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg.configure(image=self.bgImage)


