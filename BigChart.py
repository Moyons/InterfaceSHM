import tkinter as tk

import h5py
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import  FigureCanvasTkAgg, NavigationToolbar2Tk


class BigChart(tk.Toplevel):
    def __init__(self, parent, column, columnInd, chartId):
        super().__init__(parent)

        self.column = column
        self.columnInd = columnInd
        self.chartId = chartId

        self.colors = ['red', 'gold', 'lime', 'aqua']

        self.parent = parent.parent
        self.transient(self.parent)
        self.geometry("1250x700+125+30")
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.exitWindow)

        # Background Window Wallpaper
        self.image = Image.open("blue_degraded.png")
        self.imageCopy = self.image.copy()

        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg = tk.Label(self, image=self.bgImage)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.bind('<Configure>', self.resizeImage)

        self.figure = Figure(figsize=(8, 5), dpi=100, facecolor='#fcfcf7')
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        NavigationToolbar2Tk(self.figure_canvas, self)
        self.subplot = self.figure.add_subplot()

        i = 0
        for address in column:
            countChar = 0
            addressF, addressD = self.detectSymbol(address)
            with h5py.File(addressF, "a") as f:
                dset = f.get(addressD)
                valX = np.arange(0, dset.len() - 1, 1)

                for j, l in enumerate(addressD):
                    if l == "/":
                        indexSub = j
                        countChar = countChar + 1

                if indexSub != 0:
                    datasetName = addressD[(indexSub + 1):len(addressD)]

                if dset[0, 0] == 1:
                    tChannel = dset[0, 1]
                    test = "S.T. " + datasetName + " T" + str(int(tChannel))
                if dset[0, 0] == 2:
                    tChannel = dset[0, 1 + 8 * (self.columnInd - 1)]
                    test = "R.R. " + datasetName + " T" + str(int(tChannel))
                if dset[0, 0] == 3:
                    test = "P.T. " + datasetName
                if dset[0, 0] == 4:
                    test = "I.D. " + datasetName

                if dset[0, 0] == 2:
                    valY = dset[1:, self.chartId - 1 + 8 * (self.columnInd - 1)]
                else:
                    valY = dset[1:, self.chartId - 1]

                self.subplot.plot(valX, valY, color=self.colors[i], label=test + " R" + str(self.chartId))
                i += 1

        self.subplot.legend(loc='lower right')
        self.subplot.set_title("Column " + str(self.columnInd) + " - Chart " + str(self.chartId))

        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def detectSymbol(self, data):
        addressF = ""
        addressD = ""
        for n, m in enumerate(data):
            if m == '*':
                addressF = data[0: n]
                addressD = data[n + 1: len(data)]
                break
        return addressF, addressD

    def resizeImage(self, event):
        newWidth = event.width
        newHeight = event.height

        self.image = self.imageCopy.resize((newWidth, newHeight))

        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg.configure(image=self.bgImage)

    def exitWindow(self):
        self.destroy()
        self.parent.state(newstate="zoomed")
        self.parent.focus_force()
        self.parent.wm_attributes("-disabled", False)