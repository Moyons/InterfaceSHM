from PIL import Image, ImageTk
import tkinter as tk
import h5py
from tkinter_custom_button import TkinterCustomButton
from tkinter import filedialog, messagebox


class SelectHDF5(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.transient(self.parent)
        self.minsize(300, 100)
        self.geometry("800x425+400+180")
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.exitWindow)

        # Background Window Wallpaper
        self.image = Image.open("blue_degraded.png")
        self.imageCopy = self.image.copy()
        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg = tk.Label(self, image=self.bgImage)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.bind('<Configure>', self.resizeImage)

        self.lfSelectHDF5 = tk.LabelFrame(self, text="Selecting HDF5 file and group", bg='#fcfcf7')
        self.lfSelectHDF5.pack(side="top", padx=20, ipadx=200, ipady=60, pady=25)

        self.lfSelectHDF5.columnconfigure((0,1,2,3,4,5), weight=1)
        self.lfSelectHDF5.rowconfigure((0,1,2,3,4), weight=1)

        self.labelFile = tk.Label(self.lfSelectHDF5, text="File:", font=("Franklin Gothic Medium", 11), bg='#fcfcf7', borderwidth=0)
        self.labelFile.grid(column=1, row=0, padx=30, pady=10, sticky="NSEW")
        self.textAddress = tk.Text(self.lfSelectHDF5, font=("Franklin Gothic Medium",8), state=tk.DISABLED, bg='#fcfcf7', width=75, height=2)
        self.textAddress.grid(column=2, row=0, pady=10, columnspan=2)
        self.buttonFile = TkinterCustomButton(master=self.lfSelectHDF5, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=85, height=25, activebg_color="#f5f7d5", text_font=("Century Gothic", 7), text="Select File", text_color="#17181a", corner_radius=0, command=self.openFileFunction)
        self.buttonFile.grid(column=5, row=0, padx=7, pady=10)

        self.labelGroups = tk.Label(self.lfSelectHDF5, text="Groups in HDF5 file:", font=("Franklin Gothic Medium", 11), bg='#fcfcf7', borderwidth=0)
        self.labelGroups.grid(column=1, row=1, pady=15, padx=10, sticky="N")
        self.scrollGroupsY = tk.Scrollbar(self.lfSelectHDF5, orient=tk.VERTICAL)
        self.scrollGroupsX = tk.Scrollbar(self.lfSelectHDF5, orient=tk.HORIZONTAL)
        self.lbGroups = tk.Listbox(self.lfSelectHDF5, width=75, height=8, yscrollcommand=self.scrollGroupsY.set, xscrollcommand=self.scrollGroupsX.set)
        self.scrollGroupsY.configure(command=self.lbGroups.yview)
        self.scrollGroupsX.configure(command=self.lbGroups.xview)
        self.lbGroups.grid(column=2, row=1, columnspan=3)
        self.scrollGroupsY.grid(column=5, row=1, sticky="NS")
        self.scrollGroupsX.grid(column=2, row=2, pady=10, sticky="EW", columnspan=3)

        self.buttonCreateHDF5 = TkinterCustomButton(master=self.lfSelectHDF5, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 10, "bold"), text="SELECT", text_color="#17181a", corner_radius=0, width=125, command=self.selectFunction)
        self.buttonCancel = TkinterCustomButton(master=self.lfSelectHDF5, fg_color='#eb3023', border_color="#1f0404", border_width=2, activebg_color="#e87168", text_font=("Century Gothic", 10, "bold"), text="CANCEL", text_color="white", corner_radius=10, command=self.exitWindow, width=125)
        self.buttonCreateHDF5.grid(column=2, row=4)
        self.buttonCancel.grid(column=3, row=4)


    def selectFunction(self):
        addressFile = self.textAddress.get("1.0", tk.END).strip()

        if not addressFile:
            tk.messagebox.showinfo("No file", 'Select a file', parent=self)
        else:
            if not self.file.endswith('.hdf5'):
                tk.messagebox.showinfo("Error", 'You must select a HDF5 file and a group', parent=self)
            else:
                selection = self.lbGroups.curselection()
                if not selection:
                    tk.messagebox.showinfo("Error", 'You must select a group. Create one if there is no group created.', parent=self)
                else:
                    index = selection[0]

                    self.parent.textAddress.config(state=tk.NORMAL)
                    self.parent.textAddress.delete('1.0', tk.END)
                    self.parent.textAddress.insert('1.0', self.file + "   ->   " + self.groupsList[index])
                    self.parent.textAddress.config(state=tk.DISABLED)

                    self.destroy()
                    self.parent.state(newstate="zoomed")
                    self.parent.focus_force()
                    self.parent.wm_attributes("-disabled", False)


    def openFileFunction(self):
        self.groupsList = []

        self.file = filedialog.askopenfilename(title="Choose a HDF5 file", filetypes=(("*.hdf5", "*.hdf5"), ("All Files (*.*)", "*.*")))
        self.textAddress.config(state=tk.NORMAL)
        self.textAddress.delete('1.0', tk.END)
        self.textAddress.insert('1.0', self.file)
        self.textAddress.config(state=tk.DISABLED)

        self.lbGroups.delete(0, tk.END)
        if not self.file.endswith('.hdf5'):
            self.lbGroups.insert(tk.END, "\n\n\n\t\t     FILE HAS NOT HDF5 EXTENSION")
        else:
            with h5py.File(self.file, 'r') as f:
                for (path, grp) in self.h5py_group_iterator(f):
                    pathFinal = path[1:len(path)]
                    countChar = 0
                    index = 0
                    numSpace = ""

                    self.groupsList.append(path)

                    # Este bucle se utiliza para detectar si hay un grupo dentro de otro grupo

                    for i, l in enumerate(pathFinal):
                        if l == "/":
                            index = i
                            countChar = countChar + 1

                    # Así nos quedamos solo con el nombre final del grupo más pequeño
                    if index != 0:
                        pathFinal = pathFinal[(index+1):len(pathFinal)]
                        for i in range(countChar):
                            numSpace = numSpace + "      "

                    self.lbGroups.insert(tk.END, "   " + numSpace + "\u2501 " + pathFinal)

        print(self.groupsList)
        self.focus_force()


    def h5py_group_iterator(self, g, prefix=''):
        for key, item in g.items():
            path = '{}/{}'.format(prefix, key)
            if isinstance(item, h5py.Group):  # test for group
                yield (path, item)
                if isinstance(item, h5py.Group):  # test for group
                    yield from self.h5py_group_iterator(item, path)

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


