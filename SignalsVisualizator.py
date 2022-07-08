import tkinter as tk
from PIL import Image, ImageTk
import h5py
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import AddDataset
import AlgorithmWindow
import CloseDataset, ExpandChart
import HoverButton
import matplotlib.pyplot as plt
import numpy as np
import DoubleScrolledFrame


class SignalsVisualizator(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        plt.rcParams.update({'figure.max_open_warning': 0})
        self.charts = []
        self.column1 = []
        self.column2 = []
        self.column3 = []
        self.column4 = []
        self.column5 = []
        self.column6 = []
        self.column7 = []
        self.column8 = []

        self.charts.append(self.column1)
        self.charts.append(self.column2)
        self.charts.append(self.column3)
        self.charts.append(self.column4)
        self.charts.append(self.column5)
        self.charts.append(self.column6)
        self.charts.append(self.column7)
        self.charts.append(self.column8)

        self.chartsUsed = 1
        self.datasetsOpened = 0

        self.firstTime = True
        self.dataPrev = 0
        self.colors = ['red', 'gold', 'lime', 'aqua']

        # Signals Visualizator Window Configuration
        self.parent = parent
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

        # Frame Left
        self.frameLeft = tk.Frame(self, bg='#010524', borderwidth=1, relief="groove")
        self.frameLeft.pack(side="left", fill="y")
        self.frameLeft.bind('<Configure>', self.resizeFrameLeft)

        self.labelFrameLeft = tk.Label(self.frameLeft, bg='#010524')

        self.imageISATI = Image.open("ISATIlogo.jpg")
        self.imageISATI.thumbnail((110,60))
        self.imageISATIb = ImageTk.PhotoImage(self.imageISATI)
        self.labelISATI = tk.Label(self.frameLeft, image=self.imageISATIb, bg='#010524')

        self.imageAdd = Image.open("open_file.PNG")
        self.imageAdd.thumbnail((52,42))
        self.imageAdd = ImageTk.PhotoImage(self.imageAdd)
        self.buttonAddFile = HoverButton.HoverButton(self.frameLeft, image=self.imageAdd, text="   Open Dataset", font=("Franklin Gothic Medium", 10), compound="left", bg='#010524', fg="white", activebackground='#2f4854', bd=0, cursor="hand2", command=self.AddDatasetFunction)

        self.imageRem = Image.open("close_file.png")
        self.imageRem.thumbnail((52,42))
        self.imageRem = ImageTk.PhotoImage(self.imageRem)
        self.buttonRemoveFile = HoverButton.HoverButton(self.frameLeft, image=self.imageRem, text="   Close Dataset", font=("Franklin Gothic Medium", 10), compound="left", bg='#010524', fg="white", activebackground='#2f4854', bd=0, cursor="hand2", command=self.CloseDatasetFunction)

        self.imageExpand = Image.open("expand_chart.png")
        self.imageExpand.thumbnail((52, 42))
        self.imageExpand = ImageTk.PhotoImage(self.imageExpand)
        self.buttonExpandChart = HoverButton.HoverButton(self.frameLeft, image=self.imageExpand, text="   Expand Chart", font=("Franklin Gothic Medium", 10), compound="left", bg='#010524', fg="white", activebackground='#2f4854', bd=0, cursor="hand2", command=self.ExpandChartFunction)

        self.imageEdit = Image.open("edit.png")
        self.imageEdit.thumbnail((52, 42))
        self.imageEditB = ImageTk.PhotoImage(self.imageEdit)
        self.buttonEditFile = HoverButton.HoverButton(self.frameLeft, image=self.imageEditB, text="  SHM Algorithms", font=("Franklin Gothic Medium", 10), compound="left", bg='#010524', fg="white", activebackground='#2f4854', bd=0, cursor="hand2", command=self.AlgorithmWindow)

        self.imageExit = Image.open("exit.png")
        self.imageExit.thumbnail((52, 42))
        self.imageExitB = ImageTk.PhotoImage(self.imageExit)
        self.buttonExit = HoverButton.HoverButton(self.frameLeft, image=self.imageExitB, text="    Back", font=("Franklin Gothic Medium", 10), compound="left", bg='#010524', fg="white", activebackground='#2f4854', bd=0, cursor="hand2", command=self.exitWindow)

        self.createDoubleScrolledFrame()
        self.createEmptyColumn(0)
        self.firstTime = False


    def createDoubleScrolledFrame(self):
        self.frameCenter = DoubleScrolledFrame.DoubleScrolledFrame(self, borderwidth=3, relief="groove", background="#fcfcf7")
        self.frameCenter.pack(side="left", ipadx=450, ipady=200, padx=40, pady=20)

    def createEmptyColumn(self, i):
        try:
            if i == 0:
                self.fig0 = [plt.figure(figsize=(6.5, 3), dpi=75, facecolor='#fcfcf7') for i in range(8)]
                self.a0 = []
                self.canvas0 = []

                for figure in self.fig0:
                    self.a0.append(figure.add_subplot())

                j = 1
                for subplot in self.a0:
                    subplot.set_title('Column ' + str(i+1) + ' - Chart ' + str(j))
                    j += 1

                j = 0
                for figure in self.fig0:
                    canvas0 = FigureCanvasTkAgg(figure, master=self.frameCenter)
                    canvas0.get_tk_widget().configure()
                    canvas0.draw()
                    canvas0.get_tk_widget().grid(row=j, column=i, sticky="nsew")
                    j += 1

            elif i == 1:
                self.fig1 = [plt.figure(figsize=(6.5, 3), dpi=75, facecolor='#fcfcf7') for i in range(8)]
                self.a1 = []

                for figure in self.fig1:
                    self.a1.append(figure.add_subplot())

                j = 1
                for subplot in self.a1:
                    subplot.set_title('Column ' + str(i+1) + ' - Chart ' + str(j))
                    j += 1

                j = 0
                for figure in self.fig1:
                    canvas1 = FigureCanvasTkAgg(figure, master=self.frameCenter)
                    canvas1.get_tk_widget().configure()
                    canvas1.draw()
                    canvas1.get_tk_widget().grid(row=j, column=i, sticky="nsew")
                    j += 1

            elif i == 2:
                self.fig2 = [plt.figure(figsize=(6.5, 3), dpi=75, facecolor='#fcfcf7') for i in range(8)]
                self.a2 = []

                for figure in self.fig2:
                    self.a2.append(figure.add_subplot())

                j = 1
                for subplot in self.a2:
                    subplot.set_title('Column ' + str(i+1) + ' - Chart ' + str(j))
                    j += 1

                j = 0
                for figure in self.fig2:
                    canvas2 = FigureCanvasTkAgg(figure, master=self.frameCenter)
                    canvas2.get_tk_widget().configure()
                    canvas2.draw()
                    canvas2.get_tk_widget().grid(row=j, column=i, sticky="nsew")
                    j += 1

            elif i == 3:
                self.fig3 = [plt.figure(figsize=(6.5, 3), dpi=75, facecolor='#fcfcf7') for i in range(8)]
                self.a3 = []

                for figure in self.fig3:
                    self.a3.append(figure.add_subplot())

                j = 1
                for subplot in self.a3:
                    subplot.set_title('Column ' + str(i+1) + ' - Chart ' + str(j))
                    j += 1

                j = 0
                for figure in self.fig3:
                    canvas3 = FigureCanvasTkAgg(figure, master=self.frameCenter)
                    canvas3.get_tk_widget().configure()
                    canvas3.draw()
                    canvas3.get_tk_widget().grid(row=j, column=i, sticky="nsew")
                    j += 1

            elif i == 4:
                self.fig4 = [plt.figure(figsize=(6.5, 3), dpi=75, facecolor='#fcfcf7') for i in range(8)]
                self.a4 = []

                for figure in self.fig4:
                    self.a4.append(figure.add_subplot())

                j = 1
                for subplot in self.a4:
                    subplot.set_title('Column ' + str(i+1) + ' - Chart ' + str(j))
                    j += 1

                j = 0
                for figure in self.fig4:
                    canvas4 = FigureCanvasTkAgg(figure, master=self.frameCenter)
                    canvas4.get_tk_widget().configure()
                    canvas4.draw()
                    canvas4.get_tk_widget().grid(row=j, column=i, sticky="nsew")
                    j += 1

            elif i == 5:
                self.fig5 = [plt.figure(figsize=(6.5, 3), dpi=75, facecolor='#fcfcf7') for i in range(8)]
                self.a5 = []

                for figure in self.fig5:
                    self.a5.append(figure.add_subplot())

                j = 1
                for subplot in self.a5:
                    subplot.set_title('Column ' + str(i+1) + ' - Chart ' + str(j))
                    j += 1

                j = 0
                for figure in self.fig5:
                    canvas5 = FigureCanvasTkAgg(figure, master=self.frameCenter)
                    canvas5.get_tk_widget().configure()
                    canvas5.draw()
                    canvas5.get_tk_widget().grid(row=j, column=i, sticky="nsew")
                    j += 1

            elif i == 6:
                self.fig6 = [plt.figure(figsize=(6.5, 3), dpi=75, facecolor='#fcfcf7') for i in range(8)]
                self.a6 = []

                for figure in self.fig6:
                    self.a6.append(figure.add_subplot())

                j = 1
                for subplot in self.a6:
                    subplot.set_title('Column ' + str(i + 1) + ' - Chart ' + str(j))
                    j += 1

                j = 0
                for figure in self.fig6:
                    canvas6 = FigureCanvasTkAgg(figure, master=self.frameCenter)
                    canvas6.get_tk_widget().configure()
                    canvas6.draw()
                    canvas6.get_tk_widget().grid(row=j, column=i, sticky="nsew")
                    j += 1

            elif i == 7:
                self.fig7 = [plt.figure(figsize=(6.5, 3), dpi=75, facecolor='#fcfcf7') for i in range(8)]
                self.a7 = []

                for figure in self.fig7:
                    self.a7.append(figure.add_subplot())

                j = 1
                for subplot in self.a7:
                    subplot.set_title('Column ' + str(i + 1) + ' - Chart ' + str(j))
                    j += 1

                j = 0
                for figure in self.fig7:
                    canvas7 = FigureCanvasTkAgg(figure, master=self.frameCenter)
                    canvas7.get_tk_widget().configure()
                    canvas7.draw()
                    canvas7.get_tk_widget().grid(row=j, column=i, sticky="nsew")
                    j += 1
        except:
            print("Error")



    def drawCharts(self, position, column):
        addressF1 = ""
        addressD1 = ""

        countChar = 0  # Esto se utiliza para contar el número de barras que hay (número de subgrupos)
        indexSub = 0  # Esto se utiliza para guardar la posición de la barra
        datasetName = ""
        self.createEmptyColumn(position)

        for i in range(len(column)):
            text = column[i]
            for n, m in enumerate(text):
                if m == '*':
                    addressF1 = text[0: n]
                    addressD1 = text[n + 1: len(text)]
                    break

            with h5py.File(addressF1, "a") as f:
                dset = f.get(addressD1)
                valX = np.arange(0, dset.len() - 1, 1)

                for j, l in enumerate(addressD1):
                    if l == "/":
                        indexSub = j
                        countChar = countChar + 1

                if indexSub != 0:
                    datasetName = addressD1[(indexSub + 1):len(addressD1)]

                if dset[0, 0] == 1:
                    tChannel = dset[0, 1]
                    test = "S.T. " + datasetName + " T" + str(int(tChannel))
                if dset[0, 0] == 2:
                    tChannel = dset[0, 1 + 8*position]
                    test = "R.R. " + datasetName + " T" + str(int(tChannel) + 1)
                if dset[0, 0] == 3:
                    test = "P.T. " + datasetName
                if dset[0, 0] == 4:
                    test = "I.D. " + datasetName

                j = 1
                if position == 0:
                    for subplot in self.a0:
                        if dset[0, 0] == 2:
                            valY1 = dset[1:, j-1 + 8 * position]
                        else:
                            valY1 = dset[1:, j-1]

                        subplot.plot(valX, valY1, color=self.colors[i], label=test + " R" + str(j))
                        subplot.legend(loc='lower right')
                        j += 1
                elif position == 1:
                    for subplot in self.a1:
                        if dset[0, 0] == 2:
                            valY1 = dset[1:, j-1 + 8 * position]
                        else:
                            valY1 = dset[1:, j-1]
                        subplot.plot(valX, valY1, color=self.colors[i], label=test + " R" + str(j))
                        subplot.legend(loc='lower right')
                        j += 1
                elif position == 2:
                    for subplot in self.a2:
                        if dset[0, 0] == 2:
                            valY1 = dset[1:, j-1 + 8 * position]
                        else:
                            valY1 = dset[1:, j-1]
                        subplot.plot(valX, valY1, color=self.colors[i], label=test + " R" + str(j))
                        subplot.legend(loc='lower right')
                        j += 1
                elif position == 3:
                    for subplot in self.a3:
                        if dset[0, 0] == 2:
                            valY1 = dset[1:, j-1 + 8 * position]
                        else:
                            valY1 = dset[1:, j-1]
                        subplot.plot(valX, valY1, color=self.colors[i], label=test + " R" + str(j))
                        subplot.legend(loc='lower right')
                        j += 1
                elif position == 4:
                    for subplot in self.a4:
                        if dset[0, 0] == 2:
                            valY1 = dset[1:, j-1 + 8 * position]
                        else:
                            valY1 = dset[1:, j-1]
                        subplot.plot(valX, valY1, color=self.colors[i], label=test + " R" + str(j))
                        subplot.legend(loc='lower right')
                        j += 1
                elif position == 5:
                    for subplot in self.a5:
                        if dset[0, 0] == 2:
                            valY1 = dset[1:, j-1 + 8 * position]
                        else:
                            valY1 = dset[1:, j-1]
                        subplot.plot(valX, valY1, color=self.colors[i], label=test + " R" + str(j))
                        subplot.legend(loc='lower right')
                        j += 1
                elif position == 6:
                    for subplot in self.a6:
                        if dset[0, 0] == 2:
                            valY1 = dset[1:, j-1 + 8 * position]
                        else:
                            valY1 = dset[1:, j-1]
                        subplot.plot(valX, valY1, color=self.colors[i], label=test + " R" + str(j))
                        subplot.legend(loc='lower right')
                        j += 1
                elif position == 7:
                    for subplot in self.a7:
                        if dset[0, 0] == 2:
                            valY1 = dset[1:, j-1 + 8 * position]
                        else:
                            valY1 = dset[1:, j-1]
                        subplot.plot(valX, valY1, color=self.colors[i], label=test + " R" + str(j))
                        subplot.legend(loc='lower right')
                        j += 1


    def detectAsterisk(self, data):
        addressF = ""
        addressD = ""
        for n, m in enumerate(data):
            if m == '*':
                addressF = data[0: n]
                addressD = data[n + 1: len(data)]
                break
        return addressF, addressD

    def detectSymbol(self, symbol, data):
        index = 0
        for n, m in enumerate(data):
            if m == symbol:
                index = n
                break
        return index

    def deleteCharts(self, data):
        indexSymbol = self.detectSymbol("\u2501", data)
        indexArrow = self.detectSymbol(">", data)

        column = int(data[indexSymbol + 9]) - 1
        addressF = data[indexSymbol + 12: indexArrow - 2]
        addressD = data[indexArrow + 2: len(data)]
        addressFinal = addressF + "*" + addressD

        i = 0
        for address in self.charts[column]:
            if address == addressFinal:
                self.charts[column].pop(i)
                self.drawCharts(column, self.charts[column])
            i += 1

    def ExpandChartFunction(self):
        self.wm_attributes("-disabled", True)
        newWindow = ExpandChart.ExpandChart(self)
        newWindow.focus_force()

    def CloseDatasetFunction(self):
        self.wm_attributes("-disabled", True)
        newWindow = CloseDataset.CloseDataset(self)
        newWindow.focus_force()

    def AddDatasetFunction(self):
        self.wm_attributes("-disabled", True)
        newWindow = AddDataset.AddDataset(self)
        newWindow.focus_force()

    def AlgorithmWindow(self):
        newWindow = AlgorithmWindow.AlgorithmWindow(self)
        newWindow.focus_force()
        self.state(newstate="withdraw")


    def resizeImage(self, event):
        newWidth = event.width
        newHeight = event.height

        self.image = self.imageCopy.resize((newWidth, newHeight))

        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg.configure(image=self.bgImage)


    def resizeFrameLeft(self, event):
        self.labelFrameLeft.pack(side="top", padx=self.winfo_width()*0.05)
        self.labelISATI.pack(side="top", padx=self.winfo_width()*0.01, pady=self.winfo_height()*0.03)
        self.buttonAddFile.pack(side="top", pady=self.winfo_height()*0.022)
        self.buttonRemoveFile.pack(side="top", pady=self.winfo_height()*0.022)
        self.buttonExpandChart.pack(side="top", pady=self.winfo_height()*0.022)
        self.buttonEditFile.pack(side="top", pady=self.winfo_height()*0.022)
        self.buttonExit.pack(side="bottom", pady=self.winfo_height()*0.022)


    def exitWindow(self):
        plt.close('all')

        self.destroy()
        self.parent.state(newstate="zoomed")
        self.parent.focus_force()



