import globals
from PIL import Image, ImageTk
import tkinter as tk
import h5py
from tkinter_custom_button import TkinterCustomButton
from tkinter import filedialog, messagebox


class AddDataset(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.transient(self.parent)
        self.minsize(300, 100)
        self.geometry("800x500+400+160")
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.exitWindow)

        # Background Window Wallpaper
        self.image = Image.open("blue_degraded.png")
        self.imageCopy = self.image.copy()
        self.bgImage = ImageTk.PhotoImage(self.image)
        self.bg = tk.Label(self, image=self.bgImage)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.bind('<Configure>', self.resizeImage)

        self.lfSelectHDF5 = tk.LabelFrame(self, text="Selecting HDF5 file and results dataset", bg='#fcfcf7')
        self.lfSelectHDF5.pack(side="top", padx=20, ipadx=200, ipady=60, pady=25)

        self.lfSelectHDF5.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.lfSelectHDF5.rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.labelFile = tk.Label(self.lfSelectHDF5, text="File:", font=("Franklin Gothic Medium", 11), bg='#fcfcf7', borderwidth=0)
        self.labelFile.grid(column=1, row=0, padx=30, pady=10, sticky="NSEW")
        self.textAddress = tk.Text(self.lfSelectHDF5, font=("Franklin Gothic Medium", 8), state=tk.DISABLED, bg='#fcfcf7', width=75, height=2)
        self.textAddress.grid(column=2, row=0, pady=10, columnspan=2)
        self.buttonFile = TkinterCustomButton(master=self.lfSelectHDF5, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=85, height=25, activebg_color="#f5f7d5", text_font=("Century Gothic", 7), text="Select File", text_color="#17181a", corner_radius=0, command=self.openFileFunction)
        self.buttonFile.grid(column=5, row=0, padx=7, pady=10)

        self.labelGroups = tk.Label(self.lfSelectHDF5, text="Data in HDF5 file:", font=("Franklin Gothic Medium", 11), bg='#fcfcf7', borderwidth=0)
        self.labelGroups.grid(column=1, row=1, pady=15, padx=10, sticky="N")
        self.scrollGroupsY = tk.Scrollbar(self.lfSelectHDF5, orient=tk.VERTICAL)
        self.scrollGroupsX = tk.Scrollbar(self.lfSelectHDF5, orient=tk.HORIZONTAL)
        self.lbGroups = tk.Listbox(self.lfSelectHDF5, width=75, height=8, yscrollcommand=self.scrollGroupsY.set, xscrollcommand=self.scrollGroupsX.set)
        self.scrollGroupsY.configure(command=self.lbGroups.yview)
        self.scrollGroupsX.configure(command=self.lbGroups.xview)
        self.lbGroups.grid(column=2, row=1, columnspan=3)
        self.scrollGroupsY.grid(column=5, row=1, sticky="NS")
        self.scrollGroupsX.grid(column=2, row=2, pady=10, sticky="EW", columnspan=3)

        self.labelColumn = tk.Label(self.lfSelectHDF5, text="Column \n(not needed if RR test):", font=("Franklin Gothic Medium", 11), bg='#fcfcf7', borderwidth=0)
        self.labelColumn.grid(column=1, row=3, sticky="EW", pady=15)
        self.scrollColumns = tk.Scrollbar(self.lfSelectHDF5, orient=tk.VERTICAL)
        self.listboxColumns = tk.Listbox(self.lfSelectHDF5, height=2, yscrollcommand=self.scrollColumns.set, exportselection=False)
        self.scrollColumns.configure(command=self.listboxColumns.yview)
        self.listboxColumns.grid(column=2, row=3, columnspan=3, padx=5, pady=10, sticky="NSEW")
        self.scrollColumns.grid(column=5, row=3, sticky="NS")
        for i in range(self.parent.chartsUsed):
            self.listboxColumns.insert('end', 'Column %d' % (i + 1))

        self.buttonCreateHDF5 = TkinterCustomButton(master=self.lfSelectHDF5, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, activebg_color="#f5f7d5", text_font=("Century Gothic", 10, "bold"), text="SELECT", text_color="#17181a", corner_radius=0, width=125, command=self.selectFunction)
        self.buttonCancel = TkinterCustomButton(master=self.lfSelectHDF5, fg_color='#eb3023', border_color="#1f0404", border_width=2, activebg_color="#e87168", text_font=("Century Gothic", 10, "bold"), text="CANCEL", text_color="white", corner_radius=10, command=self.exitWindow, width=125)
        self.buttonCreateHDF5.grid(column=2, row=4, pady=5)
        self.buttonCancel.grid(column=3, row=4, pady=5)

    def selectFunction(self):
        selection = self.listboxColumns.curselection()
        addressFile = self.textAddress.get("1.0", tk.END).strip()

        if not addressFile:
            tk.messagebox.showinfo("No file", 'Select a file', parent=self)
        else:
            if not self.file.endswith('.hdf5'):
                tk.messagebox.showinfo("Error", 'You must select a HDF5 file and a group', parent=self)
            else:
                selectionData = self.lbGroups.curselection()
                if not selectionData:
                    tk.messagebox.showinfo("Error", 'You must select a datasets. Make a test if there is no dataset created', parent=self)
                else:
                    index = selectionData[0]

                    with h5py.File(addressFile, 'a') as f:
                        for (path, anything) in self.h5py_iterator(f):
                            if path == self.listDataResults[index]:
                                anythingFinal = str(anything)
                                # Aqui vemos si es un grupo o un dataset
                                for n, m in enumerate(anythingFinal):
                                    if m == '"':
                                        indexGD = n  # Esto se utiliza para detectar las comillas <HDF5 group "/Grupo1". Nos quedamos solo con lo de antes de las comillas
                                        anythingFinal = anythingFinal[6:indexGD - 1]
                                        break
                                if anythingFinal == "dataset":
                                    attrs = anything.attrs.keys()
                                    for n, m in enumerate(attrs):
                                        if m == "Results":
                                            if self.parent.datasetsOpened < globals.maxDatasets:
                                                if anything[0, 0] == 2:
                                                    max = 0
                                                    if len(self.parent.column1) > max:
                                                        max = len(self.parent.column1)
                                                    if len(self.parent.column2) > max:
                                                        max = len(self.parent.column2)
                                                    if len(self.parent.column3) > max:
                                                        max = len(self.parent.column3)
                                                    if len(self.parent.column4) > max:
                                                        max = len(self.parent.column4)
                                                    if len(self.parent.column5) > max:
                                                        max = len(self.parent.column5)
                                                    if len(self.parent.column6) > max:
                                                        max = len(self.parent.column6)
                                                    if len(self.parent.column7) > max:
                                                        max = len(self.parent.column7)
                                                    if len(self.parent.column8) > max:
                                                        max = len(self.parent.column8)

                                                    if max < globals.maxDatasetsChart:

                                                        self.parent.datasetsOpened += 1
                                                        self.parent.chartsUsed = 8

                                                        self.parent.column1.append(addressFile + "*" + path)
                                                        self.parent.drawCharts(0, self.parent.column1)

                                                        self.parent.column2.append(addressFile + "*" + path)
                                                        self.parent.drawCharts(1, self.parent.column2)

                                                        self.parent.column3.append(addressFile + "*" + path)
                                                        self.parent.drawCharts(2, self.parent.column3)

                                                        self.parent.column4.append(addressFile + "*" + path)
                                                        self.parent.drawCharts(3, self.parent.column4)

                                                        self.parent.column5.append(addressFile + "*" + path)
                                                        self.parent.drawCharts(4, self.parent.column5)

                                                        self.parent.column6.append(addressFile + "*" + path)
                                                        self.parent.drawCharts(5, self.parent.column6)

                                                        self.parent.column7.append(addressFile + "*" + path)
                                                        self.parent.drawCharts(6, self.parent.column7)

                                                        self.parent.column8.append(addressFile + "*" + path)
                                                        self.parent.drawCharts(7, self.parent.column8)

                                                        self.exitWindow()
                                                    else:
                                                        tk.messagebox.showinfo("Error", 'Maximum datasets in a same chart reached.', parent=self)
                                                else:
                                                    if not selection:
                                                        tk.messagebox.showinfo("Error", 'You must select a column of the visualizator.', parent=self)
                                                    else:
                                                        indexC = selection[0]
                                                        if indexC == 0:
                                                            if len(self.parent.column1) < globals.maxDatasetsChart:
                                                                self.parent.datasetsOpened += 1
                                                                self.parent.column1.append(addressFile + "*" + path)
                                                                if (indexC + 1) == self.parent.chartsUsed:
                                                                    self.parent.createEmptyColumn(1)
                                                                    self.parent.chartsUsed = 2

                                                                self.parent.drawCharts(0, self.parent.column1)
                                                                self.exitWindow()
                                                            else:
                                                                tk.messagebox.showinfo("Error", 'Maximum datasets in a same chart reached (3).', parent=self)
                                                        elif indexC == 1:
                                                            if len(self.parent.column2) < globals.maxDatasetsChart:
                                                                self.parent.datasetsOpened += 1
                                                                self.parent.column2.append(addressFile + "*" + path)
                                                                if (indexC + 1) == self.parent.chartsUsed:
                                                                    self.parent.createEmptyColumn(2)
                                                                    self.parent.chartsUsed = 3

                                                                self.parent.drawCharts(1, self.parent.column2)
                                                                self.exitWindow()
                                                            else:
                                                                tk.messagebox.showinfo("Error", 'Maximum datasets in a same chart reached.', parent=self)
                                                        elif indexC == 2:
                                                            if len(self.parent.column3) < globals.maxDatasetsChart:
                                                                self.parent.datasetsOpened += 1
                                                                self.parent.column3.append(addressFile + "*" + path)
                                                                if (indexC + 1) == self.parent.chartsUsed:
                                                                    self.parent.createEmptyColumn(3)
                                                                    self.parent.chartsUsed = 4

                                                                self.parent.drawCharts(2, self.parent.column3)
                                                                self.exitWindow()
                                                            else:
                                                                tk.messagebox.showinfo("Error", 'Maximum datasets in a same chart reached.', parent=self)
                                                        elif indexC == 3:
                                                            if len(self.parent.column4) < globals.maxDatasetsChart:
                                                                self.parent.datasetsOpened += 1
                                                                self.parent.column4.append(addressFile + "*" + path)
                                                                if (indexC + 1) == self.parent.chartsUsed:
                                                                    self.parent.createEmptyColumn(4)
                                                                    self.parent.chartsUsed = 5

                                                                self.parent.drawCharts(3, self.parent.column4)
                                                                self.exitWindow()
                                                            else:
                                                                tk.messagebox.showinfo("Error", 'Maximum datasets in a same chart reached.', parent=self)
                                                        elif indexC == 4:
                                                            if len(self.parent.column5) < globals.maxDatasetsChart:
                                                                self.parent.datasetsOpened += 1
                                                                self.parent.column5.append(addressFile + "*" + path)
                                                                if (indexC + 1) == self.parent.chartsUsed:
                                                                    self.parent.createEmptyColumn(5)
                                                                    self.parent.chartsUsed = 6

                                                                self.parent.drawCharts(4, self.parent.column5)
                                                                self.exitWindow()
                                                            else:
                                                                tk.messagebox.showinfo("Error", 'Maximum datasets in a same chart reached.', parent=self)
                                                        elif indexC == 5:
                                                            if len(self.parent.column6) < globals.maxDatasetsChart:
                                                                self.parent.datasetsOpened += 1
                                                                self.parent.column6.append(addressFile + "*" + path)
                                                                if (indexC + 1) == self.parent.chartsUsed:
                                                                    self.parent.createEmptyColumn(6)
                                                                    self.parent.chartsUsed = 7

                                                                self.parent.drawCharts(5, self.parent.column6)
                                                                self.exitWindow()
                                                            else:
                                                                tk.messagebox.showinfo("Error", 'Maximum datasets in a same chart reached.', parent=self)
                                                        elif indexC == 6:
                                                            if len(self.parent.column7) < globals.maxDatasetsChart:
                                                                self.parent.datasetsOpened += 1
                                                                self.parent.column7.append(addressFile + "*" + path)
                                                                if (indexC + 1) == self.parent.chartsUsed:
                                                                    self.parent.createEmptyColumn(7)
                                                                    self.parent.chartsUsed = 8

                                                                self.parent.drawCharts(6, self.parent.column7)
                                                                self.exitWindow()
                                                            else:
                                                                tk.messagebox.showinfo("Error", 'Maximum datasets in a same chart reached.', parent=self)
                                                        elif indexC == 7:
                                                            if len(self.parent.column8) < globals.maxDatasetsChart:
                                                                self.parent.datasetsOpened += 1
                                                                self.parent.column8.append(addressFile + "*" + path)
                                                                self.parent.drawCharts(7, self.parent.column8)
                                                                self.exitWindow()
                                                            else:
                                                                tk.messagebox.showinfo("Error", 'Maximum datasets in a same chart reached.', parent=self)
                                            else:
                                                tk.messagebox.showinfo("Error", 'Maximum datasets opened reached.', parent=self)
                                        else:
                                            tk.messagebox.showinfo("Error", 'Not a results dataset.', parent=self)
                                else:
                                    tk.messagebox.showinfo("Error", 'Select a dataset not a group.', parent=self)


    def openFileFunction(self):
        self.file = filedialog.askopenfilename(title="Choose a HDF5 file", filetypes=(("*.hdf5", "*.hdf5"), ("All Files (*.*)", "*.*")))
        self.textAddress.config(state=tk.NORMAL)
        self.textAddress.delete('1.0', tk.END)
        self.textAddress.insert('1.0', self.file)
        self.textAddress.config(state=tk.DISABLED)

        self.listDataResults = []

        self.lbGroups.delete(0, tk.END)
        if not self.file.endswith('.hdf5'):
            self.lbGroups.insert(tk.END, "\n\n\n\t\t     FILE HAS NOT HDF5 EXTENSION")
        else:
            with h5py.File(self.file, 'r+') as f:
                for (path, anything) in self.h5py_iterator(f):
                    pathFinal = path[1:len(path)]  # Esto se usa para no coger la primera barra /grupo1 por ejemplo
                    anythingFinal = str(anything)
                    countChar = 0  # Esto se utiliza para contar el número de barras que hay (número de subgrupos)
                    indexSub = 0  # Esto se utiliza para guardar la posición de la barra
                    numSpace = ""  # Esto se utiliza para añadir espacios cuando hay subgrupos y datasets

                    # Este bucle se utiliza para detectar si hay algo dentro de un grupo
                    for i, l in enumerate(pathFinal):
                        if l == "/":
                            indexSub = i
                            countChar = countChar + 1

                    # Así nos quedamos solo con el nombre final del grupo más pequeño
                    if indexSub != 0:
                        pathFinal = pathFinal[(indexSub + 1):len(pathFinal)]
                        for i in range(countChar):
                            numSpace = numSpace + "      "

                    # Aqui vemos si es un grupo o un dataset
                    for n, m in enumerate(anythingFinal):
                        if m == '"':
                            indexGD = n  # Esto se utiliza para detectar las comillas <HDF5 group "/Grupo1". Nos quedamos solo con lo de antes de las comillas
                            anythingFinal = anythingFinal[6:indexGD - 1]
                            break

                    if anythingFinal == "group":
                        self.lbGroups.insert(tk.END, "   " + numSpace + "\u2501 " + pathFinal)
                        self.listDataResults.append(path)
                    elif anythingFinal == "dataset":
                        # Aqui vemos si es un dataset de resultados o de parámetros
                        attrs = anything.attrs.keys()
                        for n, m in enumerate(attrs):
                            if m == "Results":
                                self.lbGroups.insert(tk.END, "   " + numSpace + "\u2022 " + pathFinal)
                                self.listDataResults.append(path)

        self.focus_force()

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
