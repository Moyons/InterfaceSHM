import random
from statistics import mean

from PIL import Image, ImageTk
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import BigFigureAlgorithm
from tkinter_custom_button import TkinterCustomButton
from math import sqrt
import h5py
from scipy.signal import butter, lfilter, hilbert
import os

class AlgorithmWindow(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

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

        self.files = []
        self.dataset = []

        # FRAME TOP
        self.frameTop = tk.Frame(self, bg='#d2e9fa', borderwidth=3, relief="groove")
        self.frameTop.pack(side="top", fill="x")
        self.frameTop.bind('<Configure>', self.resizeFrameTop)

        self.labelTop = tk.Label(self.frameTop, text='SHM ALGORITHMS', font=("Arial", 20, "bold", "italic"), bg='#d2e9fa')

        self.imageISATI = Image.open("ISATIlogo.jpg")
        self.imageISATI.thumbnail((120, 50))
        self.imageISATI = ImageTk.PhotoImage(self.imageISATI)
        self.labelISATI = tk.Label(self.frameTop, image=self.imageISATI, bg='#d2e9fa')

        self.imageExit = Image.open("exit.png")
        self.imageExit.thumbnail((55, 40))
        self.imageExitB = ImageTk.PhotoImage(self.imageExit)
        self.buttonExit = tk.Button(self.frameTop, image=self.imageExitB, bg='#2c526e', activebackground='#d1cce6', bd=0, cursor="hand2", command=self.exitWindow, borderwidth=1)

        # FRAME RIGHT
        self.frameLeft = tk.Frame(self, borderwidth=3, bg='#fcfcf7', relief="groove")
        self.frameLeft.pack(side="left")
        self.frameLeft.bind('<Configure>', self.resizeFrameLeft)

        # FRAME LEFT ALGORITHM
        self.frameLeftTop = tk.LabelFrame(self.frameLeft, text="Algorithms", bg='#fcfcf7', borderwidth=1)

        self.scrollAlgoY = tk.Scrollbar(self.frameLeftTop, orient=tk.VERTICAL)
        self.scrollAlgoX = tk.Scrollbar(self.frameLeftTop, orient=tk.HORIZONTAL)
        self.lbAlgorithms = tk.Listbox(self.frameLeftTop, width=40, height=15, yscrollcommand=self.scrollAlgoY.set, xscrollcommand=self.scrollAlgoX.set, exportselection=False)
        self.scrollAlgoY.configure(command=self.lbAlgorithms.yview)
        self.scrollAlgoX.configure(command=self.lbAlgorithms.xview)

        self.addAlgorithmsLB()

        # FRAME LEFT DATASETS
        self.frameLeftBot = tk.LabelFrame(self.frameLeft, text="Datasets", bg='#fcfcf7', borderwidth=1)

        self.scrollDatasetsY = tk.Scrollbar(self.frameLeftBot, orient=tk.VERTICAL)
        self.scrollDatasetsX = tk.Scrollbar(self.frameLeftBot, orient=tk.HORIZONTAL)
        self.lbCharts = tk.Listbox(self.frameLeftBot, width=40, height=15, yscrollcommand=self.scrollDatasetsY.set, xscrollcommand=self.scrollDatasetsX.set, exportselection=False)
        self.scrollDatasetsY.configure(command=self.lbCharts.yview)
        self.scrollDatasetsX.configure(command=self.lbCharts.xview)

        self.addChartsLB()

        self.frameCenter = tk.Frame(self, bg='#fcfcf7', borderwidth=3, relief="groove")
        self.frameCenter.pack(side="left")
        self.frameCenter.bind('<Configure>', self.resizeFrameCenter)

        self.Piezo1 = tk.Label(self.frameCenter, text="Piezo 1:", font=("Arial", 9), bg='#fcfcf7', borderwidth=0)
        self.Piezo2 = tk.Label(self.frameCenter, text="Piezo 2:", font=("Arial", 9), bg='#fcfcf7', borderwidth=0)
        self.Piezo3 = tk.Label(self.frameCenter, text="Piezo 3:", font=("Arial", 9), bg='#fcfcf7', borderwidth=0)
        self.Piezo4 = tk.Label(self.frameCenter, text="Piezo 4:", font=("Arial", 9), bg='#fcfcf7', borderwidth=0)
        self.Piezo5 = tk.Label(self.frameCenter, text="Piezo 5:", font=("Arial", 9), bg='#fcfcf7', borderwidth=0)
        self.Piezo6 = tk.Label(self.frameCenter, text="Piezo 6:", font=("Arial", 9), bg='#fcfcf7', borderwidth=0)
        self.Piezo7 = tk.Label(self.frameCenter, text="Piezo 7:", font=("Arial", 9), bg='#fcfcf7', borderwidth=0)
        self.Piezo8 = tk.Label(self.frameCenter, text="Piezo 8:", font=("Arial", 9), bg='#fcfcf7', borderwidth=0)

        self.P1X = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P1X.insert(0, 'X (m)')
        self.P2X = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P2X.insert(0, 'X (m)')
        self.P3X = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P3X.insert(0, 'X (m)')
        self.P4X = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P4X.insert(0, 'X (m)')
        self.P5X = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P5X.insert(0, 'X (m)')
        self.P6X = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P6X.insert(0, 'X (m)')
        self.P7X = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P7X.insert(0, 'X (m)')
        self.P8X = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P8X.insert(0, 'X (m)')

        self.P1Y = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P1Y.insert(0, 'Y (m)')
        self.P2Y = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P2Y.insert(0, 'Y (m)')
        self.P3Y = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P3Y.insert(0, 'Y (m)')
        self.P4Y = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P4Y.insert(0, 'Y (m)')
        self.P5Y = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P5Y.insert(0, 'Y (m)')
        self.P6Y = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P6Y.insert(0, 'Y (m)')
        self.P7Y = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P7Y.insert(0, 'Y (m)')
        self.P8Y = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.P8Y.insert(0, 'Y (m)')

        self.canvas1 = tk.Canvas(self.frameCenter, bg='#737370')

        self.speed = tk.Label(self.frameCenter, text="Speed:", font=("Arial", 9), bg='#fcfcf7', borderwidth=0)
        self.speedEntry = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.speedEntry.insert(0, 'm/s')
        self.initSamples = tk.Label(self.frameCenter, text="Samples ignored:", font=("Arial", 9), bg='#fcfcf7', borderwidth=0)
        self.initSamEntry = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.initSamEntry.insert(0, 'Samples')

        self.canvas2 = tk.Canvas(self.frameCenter, bg='#737370')

        self.zone = tk.Label(self.frameCenter, text="Inspection zone:", font=("Arial", 9), bg='#fcfcf7', borderwidth=0)
        self.zoneXmin = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.zoneXmin.insert(0, 'X min (m)')
        self.zoneXmax = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.zoneXmax.insert(0, 'X max (m)')
        self.zoneYmin = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.zoneYmin.insert(0, 'Y min (m)')
        self.zoneYmax = tk.Entry(self.frameCenter, font=("Arial", 9), borderwidth=1, relief="solid", width=15)
        self.zoneYmax.insert(0, 'Y max (m)')

        # FRAME RIGHT
        self.frameRight = tk.Frame(self, bg='#fcfcf7', borderwidth=3, relief="groove")
        self.frameRight.pack(side="left", padx=8, pady=10)

        #data = np.random.random([100, 100]) * 1 # Lo de * 1 es para creartelos entre 0 y 1
        data = np.random.random([100, 100]) * 0
        self.figure2D = plt.figure(figsize=(5.5, 4))
        ax = self.figure2D.add_subplot(111)
        c = ax.pcolor(data, cmap='rainbow', shading='auto')
        self.figure2D.colorbar(c)

        canvasFigure2D = FigureCanvasTkAgg(self.figure2D, master=self.frameRight)
        canvasFigure2D.draw()
        canvasFigure2D.get_tk_widget().grid(row=0, column=0, columnspan=4, sticky="nsew")

        self.buttonExecute = TkinterCustomButton(master=self.frameRight, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 10, "bold"), text="EXECUTE", text_color="#17181a", corner_radius=0, width=100, command=self.executeAlgorithm)
        self.buttonExpand = TkinterCustomButton(master=self.frameRight, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 10, "bold"), text="EXPAND", text_color="#17181a", corner_radius=0, width=100, command=self.expandFigure)

        self.buttonExecute.grid(column=1, row=1, padx=3, pady=8)
        self.buttonExpand.grid(column=2, row=1, padx=3, pady=8)

    def executeAlgorithm(self):
        selection1 = self.lbAlgorithms.curselection()
        selection2 = self.lbCharts.curselection()

        self.x1 = self.P1X.get()
        self.x2 = self.P2X.get()
        self.x3 = self.P3X.get()
        self.x4 = self.P4X.get()
        self.x5 = self.P5X.get()
        self.x6 = self.P6X.get()
        self.x7 = self.P7X.get()
        self.x8 = self.P8X.get()

        self.y1 = self.P1Y.get()
        self.y2 = self.P2Y.get()
        self.y3 = self.P3Y.get()
        self.y4 = self.P4Y.get()
        self.y5 = self.P5Y.get()
        self.y6 = self.P6Y.get()
        self.y7 = self.P7Y.get()
        self.y8 = self.P8Y.get()

        self.sp = self.speedEntry.get()
        self.sampl = self.initSamEntry.get()

        self.zx1 = self.zoneXmin.get()
        self.zx2 = self.zoneXmax.get()
        self.zy1 = self.zoneYmin.get()
        self.zy2 = self.zoneYmax.get()

        if not selection1:
            tk.messagebox.showinfo("Error", 'You must select an algorithm', parent=self)
        elif not selection2:
            tk.messagebox.showinfo("Error", 'You must select a dataset', parent=self)
        else:
            if not self.isFloat(self.x1):
                tk.messagebox.showinfo("Error piezo 1", 'Position x of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.x2):
                tk.messagebox.showinfo("Error piezo 2", 'Position x of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.x3):
                tk.messagebox.showinfo("Error piezo 3", 'Position x of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.x4):
                tk.messagebox.showinfo("Error piezo 4", 'Position x of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.x5):
                tk.messagebox.showinfo("Error piezo 5", 'Position x of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.x6):
                tk.messagebox.showinfo("Error piezo 6", 'Position x of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.x7):
                tk.messagebox.showinfo("Error piezo 7", 'Position x of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.x8):
                tk.messagebox.showinfo("Error piezo 8", 'Position x of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.y1):
                tk.messagebox.showinfo("Error piezo 1", 'Position y of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.y2):
                tk.messagebox.showinfo("Error piezo 2", 'Position y of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.y3):
                tk.messagebox.showinfo("Error piezo 3", 'Position y of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.y4):
                tk.messagebox.showinfo("Error piezo 4", 'Position y of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.y5):
                tk.messagebox.showinfo("Error piezo 5", 'Position y of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.y6):
                tk.messagebox.showinfo("Error piezo 6", 'Position y of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.y7):
                tk.messagebox.showinfo("Error piezo 7", 'Position y of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.y8):
                tk.messagebox.showinfo("Error piezo 8", 'Position x of Piezo must be an decimal number', parent=self)
            elif not self.isFloat(self.sp):
                tk.messagebox.showinfo("Error speed", 'Propagation speed must be a number', parent=self)
            elif not self.isInt(self.sampl):
                tk.messagebox.showinfo("Error init samples", 'Samples ignored must be an intenger number', parent=self)
            elif not self.isFloat(self.zx1) or not self.isFloat(self.zx2) or not self.isFloat(self.zy1) or not self.isFloat(self.zy2):
                tk.messagebox.showinfo("Error specific zone", 'Dimensions of specific zone must be a number', parent=self)
            elif self.zx1 > self.zx2:
                tk.messagebox.showinfo("Error specific zone x", 'x1 can not be bigger than x2', parent=self)
            elif self.zy1 > self.zy2:
                tk.messagebox.showinfo("Error specific zone y", 'y1 can not be bigger than y2', parent=self)
            else:
                self.algorithm()

    def algorithm(self):
        fs = 40*pow(10, 6)
        nSensors = 8
        vp = float(self.sp)
        cutoffL = 1000000

        piezos = np.zeros((nSensors, 2))
        realFinal = np.zeros((25000, 8, 8))
        imagFinal = np.zeros((25000, 8, 8))

        piezos[0][0] = float(self.x1)
        piezos[1][0] = float(self.x2)
        piezos[2][0] = float(self.x3)
        piezos[3][0] = float(self.x4)
        piezos[4][0] = float(self.x5)
        piezos[5][0] = float(self.x6)
        piezos[6][0] = float(self.x7)
        piezos[7][0] = float(self.x8)

        piezos[0][1] = float(self.y1)
        piezos[1][1] = float(self.y2)
        piezos[2][1] = float(self.y3)
        piezos[3][1] = float(self.y4)
        piezos[4][1] = float(self.y5)
        piezos[5][1] = float(self.y6)
        piezos[6][1] = float(self.y7)
        piezos[7][1] = float(self.y8)

        selection = self.lbCharts.curselection()
        index = selection[0]

        xMin = float(self.zx1)
        xMax = float(self.zx2)
        yMin = float(self.zy1)
        yMax = float(self.zy2)

        tx = 0
        rx = 0

        initialSamples = int(self.sampl)

        with h5py.File(self.files[index], 'a') as f: # f es el fichero con el dataset al que se quiere realizar el algoritmo
            for (path, anything) in self.h5py_iterator(f):
                if path == self.dataset[index]:
                    samples = anything.len() - initialSamples

                    for col in range(64):
                        data = anything[initialSamples - 1:(anything.len() - 1), col]

                        yFiltL = self.butter_lowpass_filter(data, cutoffL, fs)
                        yFiltH = yFiltL - mean(yFiltL)
                        yHilt = hilbert(yFiltH)

                        for i in range(samples):
                            realFinal[i][tx][rx] = np.real(yHilt[i])
                            imagFinal[i][tx][rx] = np.imag(yHilt[i])

                        rx = rx + 1

                        if rx == nSensors:
                            rx = 0
                            tx = tx + 1

        div = 100

        xSamples = div
        ySamples = div

        dmin = 0.00
        off = 1  # off=0, all signals, off=1, ignoring pulse echo signals transmitter==receiver

        x = np.linspace(xMin, xMax, xSamples)
        y = np.linspace(yMin, yMax, ySamples)

        dataFinal = np.zeros((xSamples, ySamples))

        for i in range(xSamples):
            for j in range(ySamples):
                auxReal = 0
                auxImag = 0
                for t in range(nSensors):
                    for r in range(t + off, nSensors):
                        d1 = sqrt(pow(x[i] - piezos[t, 0], 2) + pow(y[j] - piezos[t, 1], 2))
                        d2 = sqrt(pow(x[i] - piezos[r, 0], 2) + pow(y[j] - piezos[r, 1], 2))
                        sampleAnalyzed = round(((d1 + d2) / vp) * fs) + 1
                        # print("i " + str(i) + " j " + str(j) + " D1 " + str(d1) + " D2 " + str(d2) + " Sample_ana " + str(sampleAnalyzed) + " x " + str(x[i]) + " y " + str(y[i]) + " tx " + str(t) + " rx " + str(r) + " " + str(piezos[t, 0]) + " " + str(piezos[t, 1]))

                        if d1 > dmin and d2 > dmin and samples > sampleAnalyzed:
                            auxReal = auxReal + realFinal[sampleAnalyzed][t][r] + realFinal[sampleAnalyzed][r][t]  # Este valor no puede ser igual antes que después
                            auxImag = auxImag + imagFinal[sampleAnalyzed][t][r] + imagFinal[sampleAnalyzed][r][t]
                            # print("auxReal " + str(auxReal) + " auxImag " + str(auxImag))
                # print(auxReal)
                # print(auxImag)
                dataFinal[i][j] = sqrt(pow(auxReal, 2) + pow(auxImag, 2))

        tk.messagebox.showinfo("Correct", 'Algorithm correctly done!', parent=self)

        self.figure2D, ax = plt.subplots()
        c = ax.pcolor(x, y, np.transpose(dataFinal), cmap='jet', shading='auto')
        self.figure2D.colorbar(c)

        canvasFigure2D = FigureCanvasTkAgg(self.figure2D, master=self.frameRight)
        canvasFigure2D.draw()
        canvasFigure2D.get_tk_widget().grid(row=0, column=0, columnspan=4, sticky="nsew")


    def expandFigure(self):
        self.wm_attributes("-disabled", True)
        newWindow = BigFigureAlgorithm.BigFigureAlgorithm(self, self.figure2D)
        newWindow.focus_force()

    def resizeFrameCenter(self, event=0):
        self.frameCenter.pack(padx=self.winfo_width() * 0.015, pady=self.winfo_height() * 0.04)

        self.Piezo1.grid(column=0, row=0, padx=10, pady=8)
        self.Piezo2.grid(column=0, row=1, padx=10, pady=8)
        self.Piezo3.grid(column=0, row=2, padx=10, pady=8)
        self.Piezo4.grid(column=0, row=3, padx=10, pady=8)
        self.Piezo5.grid(column=0, row=4, padx=10, pady=8)
        self.Piezo6.grid(column=0, row=5, padx=10, pady=8)
        self.Piezo7.grid(column=0, row=6, padx=10, pady=8)
        self.Piezo8.grid(column=0, row=7, padx=10, pady=8)

        self.P1X.grid(column=1, row=0, ipady=5, padx=10, pady=8)
        self.P2X.grid(column=1, row=1, ipady=5, padx=10, pady=8)
        self.P3X.grid(column=1, row=2, ipady=5, padx=10, pady=8)
        self.P4X.grid(column=1, row=3, ipady=5, padx=10, pady=8)
        self.P5X.grid(column=1, row=4, ipady=5, padx=10, pady=8)
        self.P6X.grid(column=1, row=5, ipady=5, padx=10, pady=8)
        self.P7X.grid(column=1, row=6, ipady=5, padx=10, pady=8)
        self.P8X.grid(column=1, row=7, ipady=5, padx=10, pady=8)

        self.P1Y.grid(column=2, row=0, ipady=5, padx=10, pady=8)
        self.P2Y.grid(column=2, row=1, ipady=5, padx=10, pady=8)
        self.P3Y.grid(column=2, row=2, ipady=5, padx=10, pady=8)
        self.P4Y.grid(column=2, row=3, ipady=5, padx=10, pady=8)
        self.P5Y.grid(column=2, row=4, ipady=5, padx=10, pady=8)
        self.P6Y.grid(column=2, row=5, ipady=5, padx=10, pady=8)
        self.P7Y.grid(column=2, row=6, ipady=5, padx=10, pady=8)
        self.P8Y.grid(column=2, row=7, ipady=5, padx=10, pady=8)

        self.canvas1.config(width=self.winfo_width()*0.15, height=self.winfo_height()*0.002)
        self.canvas1.grid(column=0, row=8, columnspan=3, pady=self.winfo_height() * 0.02)

        self.speed.grid(column=0, row=9, ipady=5, padx=10, pady=8)
        self.speedEntry.grid(column=1, row=9, ipady=5, padx=10, pady=8)
        self.initSamples.grid(column=0, row=10, ipady=5, padx=10, pady=8)
        self.initSamEntry.grid(column=1, row=10, ipady=5, padx=10, pady=8)

        self.canvas2.config(width=self.winfo_width()*0.15, height=self.winfo_height()*0.002)
        self.canvas2.grid(column=0, row=11, columnspan=3, pady=self.winfo_height() * 0.02)

        self.zone.grid(column=0, row=12, padx=10, pady=8)
        self.zoneXmin.grid(column=1, row=12, ipady=5, padx=10, pady=8)
        self.zoneXmax.grid(column=2, row=12, ipady=5, padx=10, pady=8)
        self.zoneYmin.grid(column=1, row=13, ipady=5, padx=10, pady=8)
        self.zoneYmax.grid(column=2, row=13, ipady=5, padx=10, pady=8)

    def resizeFrameLeft(self, event=0):
        self.frameLeft.pack(padx=self.winfo_width()*0.03, pady=self.winfo_height()*0.04)

        self.frameLeftTop.pack(side="top", padx=self.winfo_width()*0.025, pady=self.winfo_height()*0.012)
        self.frameLeftBot.pack(side="top", padx=self.winfo_width() * 0.025, pady=self.winfo_height() * 0.012)

        self.lbAlgorithms.grid(column=1, row=0, columnspan=3, padx=self.winfo_width() * 0.025, pady=self.winfo_height() * 0.012)
        self.scrollAlgoY.grid(column=4, row=0, sticky="NS")
        self.scrollAlgoX.grid(column=1, row=1, sticky="EW", columnspan=3)

        self.lbCharts.grid(column=1, row=0, columnspan=3, padx=self.winfo_width() * 0.025, pady=self.winfo_height() * 0.012)
        self.scrollDatasetsY.grid(column=4, row=0, sticky="NS")
        self.scrollDatasetsX.grid(column=1, row=1, sticky="EW", columnspan=3)

    def addAlgorithmsLB(self):
        self.lbAlgorithms.insert('end', "      \u2501 Correlation Based Imaging ")

    def addChartsLB(self):
        allDatasets = []

        for columns in self.parent.charts:
            for datasets in columns:
                addressF, addressD = self.detectSymbol(datasets)
                dataset = addressF + " -> " + addressD
                if not dataset in allDatasets:
                    with h5py.File(addressF, 'a') as f:
                        for (path, anything) in self.h5py_iterator(f):
                            if path == addressD:
                                if anything[0, 0] == 2:
                                    allDatasets.append(dataset)
                                    self.lbCharts.insert('end', "      \u2501 " + dataset)

                                    self.files.append(addressF)
                                    self.dataset.append(addressD)

    def butter_lowpass(self, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def detectSymbol(self, data):
        addressF = ""
        addressD = ""
        for n, m in enumerate(data):
            if m == '*':
                addressF = data[0: n]
                addressD = data[n + 1: len(data)]
                break
        return addressF, addressD

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

    def resizeFrameTop(self, event=0):
        self.labelTop.pack(side="left", padx=self.winfo_width()*0.035, pady=self.winfo_height()*0.025)
        self.labelISATI.pack(side="left", padx=self.winfo_width()*0.22)
        self.buttonExit.pack(side="right", padx=self.winfo_width()*0.02)

    def h5py_iterator(self, g, prefix=''):
        for key, item in g.items():
            path = '{}/{}'.format(prefix, key)
            if isinstance(item, h5py.Group) or isinstance(item, h5py.Dataset):
                yield (path, item)
                if isinstance(item, h5py.Group):
                    yield from self.h5py_iterator(item, path)

    def isFloat(self, elemento):
        try:
            float(elemento)
            return True
        except ValueError:
            return False

    def isInt(self, elemento):
        try:
            int(elemento)
            return True
        except ValueError:
            return False


