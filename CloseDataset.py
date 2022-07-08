from PIL import Image, ImageTk
import tkinter as tk
import h5py
from tkinter_custom_button import TkinterCustomButton


class CloseDataset(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.transient(self.parent)
        self.minsize(300, 100)
        self.geometry("800x430+400+150")
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.exitWindow)

        # Background Window Wallpaper
        self.image = Image.open("blue_degraded.png")
        self.imageCopy = self.image.copy()
        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg = tk.Label(self, image=self.bgImage)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.bind('<Configure>', self.resizeImage)

        self.lfCloseDataset = tk.LabelFrame(self, text="Closing HDF5 file and results dataset", bg='#fcfcf7')
        self.lfCloseDataset.pack(side="top", padx=20, ipadx=200, ipady=60, pady=25)

        self.lfCloseDataset.columnconfigure((0,1,2,3,4), weight=1)
        self.lfCloseDataset.rowconfigure((0,1,2,3,4), weight=1)

        self.labelDatasets = tk.Label(self.lfCloseDataset, text="Opened datasets:", font=("Franklin Gothic Medium", 11), bg='#fcfcf7', borderwidth=0)
        self.labelDatasets.grid(column=0, row=0, pady=20, padx=7, sticky="N")
        self.scrollDatasetsY = tk.Scrollbar(self.lfCloseDataset, orient=tk.VERTICAL)
        self.scrollDatasetsX = tk.Scrollbar(self.lfCloseDataset, orient=tk.HORIZONTAL)
        self.lbDatasets = tk.Listbox(self.lfCloseDataset, width=90, height=15, yscrollcommand=self.scrollDatasetsY.set, xscrollcommand=self.scrollDatasetsX.set, selectmode="multiple")
        self.scrollDatasetsY.configure(command=self.lbDatasets.yview)
        self.scrollDatasetsX.configure(command=self.lbDatasets.xview)
        self.lbDatasets.grid(column=1, row=0, columnspan=3, pady=15)
        self.scrollDatasetsY.grid(column=4, row=0, sticky="NS")
        self.scrollDatasetsX.grid(column=1, row=1, sticky="EW", columnspan=3)

        self.addDatasetsLB()

        self.buttonClose = TkinterCustomButton(master=self.lfCloseDataset, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 10, "bold"), text="SELECT", text_color="#17181a", corner_radius=0, width=125, command=self.closeDatasets)
        self.buttonCancel = TkinterCustomButton(master=self.lfCloseDataset, fg_color='#eb3023', border_color="#1f0404", border_width=2, activebg_color="#e87168", text_font=("Century Gothic", 10, "bold"), text="CANCEL", text_color="white", corner_radius=10, width=125, command=self.exitWindow)

        self.buttonClose.grid(column=1, row=2, pady=15)
        self.buttonCancel.grid(column=2, row=2, pady=15)

    def closeDatasets(self):
        valuesSelected = [self.lbDatasets.get(index) for index in self.lbDatasets.curselection()]

        for data in valuesSelected:
            self.parent.deleteCharts(data)

        self.exitWindow()

    def addDatasetsLB(self):
        i = 1
        for columns in self.parent.charts:
            for datasets in columns:
                addressF, addressD = self.detectSymbol(datasets)
                self.lbDatasets.insert('end', "      \u2501 Column " + str(i) + ": " + addressF + " -> " + addressD)
            i += 1

    def detectSymbol(self, data):
        addressF = ""
        addressD = ""
        for n, m in enumerate(data):
            if m == '*':
                addressF = data[0: n]
                addressD = data[n + 1: len(data)]
                break
        return addressF, addressD


    def h5py_iterator(self, g, prefix=''):
        for key, item in g.items():
            path = '{}/{}'.format(prefix, key)
            if isinstance(item, h5py.Group) or isinstance(item, h5py.Dataset):
                yield (path, item)
                if isinstance(item, h5py.Group):
                    yield from self.h5py_iterator(item, path)

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