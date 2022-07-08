import tkinter as tk
from PIL import Image, ImageTk
import BigChart

from tkinter_custom_button import TkinterCustomButton

class ExpandChart(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.transient(self.parent)
        self.minsize(300, 100)
        self.geometry("650x430+450+160")
        self.resizable(0,0)
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

        self.labelDatasets = tk.Label(self.lfCloseDataset, text="Charts available:", font=("Franklin Gothic Medium", 11), bg='#fcfcf7', borderwidth=0)
        self.labelDatasets.grid(column=0, row=0, pady=20, padx=7, sticky="N")
        self.scrollDatasetsY = tk.Scrollbar(self.lfCloseDataset, orient=tk.VERTICAL)
        self.scrollDatasetsX = tk.Scrollbar(self.lfCloseDataset, orient=tk.HORIZONTAL)
        self.lbCharts = tk.Listbox(self.lfCloseDataset, width=70, height=15, yscrollcommand=self.scrollDatasetsY.set, xscrollcommand=self.scrollDatasetsX.set)
        self.scrollDatasetsY.configure(command=self.lbCharts.yview)
        self.scrollDatasetsX.configure(command=self.lbCharts.xview)
        self.lbCharts.grid(column=1, row=0, columnspan=3, pady=15)
        self.scrollDatasetsY.grid(column=4, row=0, sticky="NS")
        self.scrollDatasetsX.grid(column=1, row=1, sticky="EW", columnspan=3)

        self.addChartsLB()

        self.buttonExpand = TkinterCustomButton(master=self.lfCloseDataset, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 10, "bold"), text="EXPAND", text_color="#17181a", corner_radius=0, width=125, command=self.expandFunction)
        self.buttonCancel = TkinterCustomButton(master=self.lfCloseDataset, fg_color='#eb3023', border_color="#1f0404", border_width=2, activebg_color="#e87168", text_font=("Century Gothic", 10, "bold"), text="CANCEL", text_color="white", corner_radius=10, width=125, command=self.exitWindow)

        self.buttonExpand.grid(column=1, row=2, pady=15)
        self.buttonCancel.grid(column=2, row=2, pady=15)

    def expandFunction(self):
        selection = self.lbCharts.curselection()
        index = selection[0]
        valueSelection = self.lbCharts.get(index)
        columnInd = 0
        chartId = 0

        for n, m in enumerate(valueSelection):
            if m == "\u2501":
                columnInd = int(valueSelection[n + 9])
                chartId = int(valueSelection[n + 19])
                break

        newWindow = BigChart.BigChart(self, self.parent.charts[columnInd - 1], columnInd, chartId)
        newWindow.focus_force()
        self.state(newstate="withdraw")

    def addChartsLB(self):
        i = 1
        for column in self.parent.charts:
            if column:
                for j in range(8):
                    self.lbCharts.insert('end', "      \u2501 Column " + str(i) + " - Chart " + str(j + 1))
            i += 1

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