from PIL import Image, ImageTk
import tkinter as tk
import h5py
from tkinter_custom_button import TkinterCustomButton
from tkinter import filedialog, messagebox

class ConfigureHDF5(tk.Toplevel):

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

        # FRAME TOP
        self.frameTop = tk.Frame(self, bg='#d2e9fa', borderwidth=3, relief="groove")
        self.frameTop.pack(side="top", fill="x")
        self.frameTop.bind('<Configure>', self.resizeFrameTop)

        self.labelTop = tk.Label(self.frameTop, text='CONFIGURE HDF5 FILES', font=("Arial", 20, "bold", "italic"), bg='#d2e9fa')

        self.imageISATI = Image.open("ISATIlogo.jpg")
        self.imageISATI.thumbnail((120,50))
        self.imageISATI = ImageTk.PhotoImage(self.imageISATI)
        self.labelISATI = tk.Label(self.frameTop, image=self.imageISATI, bg='#d2e9fa')

        self.imageExit = Image.open("house.png")
        self.imageExit.thumbnail((62, 50))
        self.imageExitB = ImageTk.PhotoImage(self.imageExit)
        self.buttonExit = tk.Button(self.frameTop, image=self.imageExitB, bg='#d2e9fa', activebackground='#d1cce6', bd=0, cursor="hand2", command=self.exitWindow, borderwidth=1)



        # FRAME LEFT
        self.frameLeft = tk.Frame(self, bg='#fcfcf7', borderwidth=3, relief="groove")
        self.frameLeft.pack(side="left")
        self.frameLeft.bind('<Configure>', self.resizeFrameLeft)

        self.frameLeft.columnconfigure((0,1,2,3,4,5,6,7), weight=1)
        self.frameLeft.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14), weight=1)

        self.labelFile1 = tk.Label(self.frameLeft, text="File 1:", bg='#fcfcf7', borderwidth=0)
        self.textAddress1 = tk.Text(self.frameLeft, state=tk.DISABLED, bg='#fcfcf7')
        self.buttonFile1 = TkinterCustomButton(master=self.frameLeft)
        # Hay que crear el botón primero para poder olvidar su posición cada vez que se ajusta la ventana y sobreescribir la posición actual
        # en base a las medidas de la ventana

        self.scrollGroupsY1 = tk.Scrollbar(self.frameLeft, orient=tk.VERTICAL)
        self.scrollGroupsX1 = tk.Scrollbar(self.frameLeft, orient=tk.HORIZONTAL)
        self.lb1 = tk.Listbox(self.frameLeft, yscrollcommand=self.scrollGroupsY1.set, xscrollcommand=self.scrollGroupsX1.set, exportselection=False)
        self.scrollGroupsY1.configure(command=self.lb1.yview)
        self.scrollGroupsX1.configure(command=self.lb1.xview)

        self.lfaddGroup1 = tk.LabelFrame(self.frameLeft, text="Adding new Group", bg='#fcfcf7')
        self.lfaddGroup1.columnconfigure((0,1,2,3), weight=1)
        self.lfaddGroup1.rowconfigure((0,1,2), weight=1)
        self.labelFileNameG1 = tk.Label(self.lfaddGroup1, text="Group name:", font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textFileNameG1 = tk.Entry(self.lfaddGroup1, borderwidth=1, font=("Franklin Gothic Medium", 9), relief="solid")
        self.labelAddressG1 = tk.Label(self.lfaddGroup1, text='Address ("/" between groups):', font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textAddressG1 = tk.Entry(self.lfaddGroup1, borderwidth=1, font=("Franklin Gothic Medium", 9), relief="solid")
        self.textAddressG1.insert(0, 'Example: "/Group1/Group2"')
        self.buttonAddG1 = TkinterCustomButton(master=self.lfaddGroup1)

        self.lfDelete1 = tk.LabelFrame(self.frameLeft, text="Delete dataset/group", bg='#fcfcf7')
        self.lfDelete1.columnconfigure((0,1,2,3), weight=1)
        self.lfDelete1.rowconfigure((0,1,2), weight=1)
        self.labelAddressD1 = tk.Label(self.lfDelete1, text='Address ("/" between groups):', font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textAddressD1 = tk.Entry(self.lfDelete1, borderwidth=1, font=("Franklin Gothic Medium", 9), relief="solid")
        self.textAddressD1.insert(0, 'Example: "/Group1/Group2"')
        self.buttonAddD1 = TkinterCustomButton(master=self.lfDelete1)

        self.lfmoveSomething1 = tk.LabelFrame(self.frameLeft, text="Moving dataset/group", bg='#fcfcf7')
        self.lfmoveSomething1.columnconfigure((0,1,2,3), weight=1)
        self.lfmoveSomething1.rowconfigure((0,1,2,3), weight=1)
        self.labelInitAddressM1 = tk.Label(self.lfmoveSomething1, text='Init Addr ("/" between groups):', font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textInitAddressM1 = tk.Entry(self.lfmoveSomething1, borderwidth=1, relief="solid")
        self.textInitAddressM1.insert(0, 'Example: "/Group1/Group2/DatasetInit"')
        self.labelEndAddressM1 = tk.Label(self.lfmoveSomething1, text='End Addr ("/" between groups):', font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textEndAddressM1 = tk.Entry(self.lfmoveSomething1, borderwidth=1, font=("Franklin Gothic Medium", 9), relief="solid")
        self.textEndAddressM1.insert(0, 'Example: "/Group1/Group3')
        self.labelNewNameM1 = tk.Label(self.lfmoveSomething1, text="Name in new address:", font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textNewNameM1 = tk.Entry(self.lfmoveSomething1, borderwidth=1, relief="solid")
        self.buttonMove1 = TkinterCustomButton(master=self.lfmoveSomething1)

        self.lfcopySomething1 = tk.LabelFrame(self.frameLeft, text="Copying dataset/group", bg='#fcfcf7')
        self.lfcopySomething1.columnconfigure((0,1,2,3), weight=1)
        self.lfcopySomething1.rowconfigure((0,1,2,3,4), weight=1)
        self.labelInitAddressC1 = tk.Label(self.lfcopySomething1, text='Init Addr ("/" between groups):', font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textInitAddressC1 = tk.Entry(self.lfcopySomething1, borderwidth=1, relief="solid")
        self.textInitAddressC1.insert(0, 'Example: "/Group1/Group2/DatasetInit"')
        self.labelEndAddressC1 = tk.Label(self.lfcopySomething1, text='End Addr ("/" between groups):', font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textEndAddressC1 = tk.Entry(self.lfcopySomething1, borderwidth=1, font=("Franklin Gothic Medium", 9), relief="solid")
        self.textEndAddressC1.insert(0, 'Example: "/Group1/Group3')
        self.labelNewNameC1 = tk.Label(self.lfcopySomething1, text="Name in new address:", font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textNewNameC1 = tk.Entry(self.lfcopySomething1, borderwidth=1, relief="solid")
        self.file1To2 = tk.IntVar()
        self.buttonCheckCopy1 = tk.Checkbutton(self.lfcopySomething1, text="Copying from file 1 to 2", variable=self.file1To2, onvalue=1, offvalue=0)
        self.buttonCopy1 = TkinterCustomButton(master=self.lfcopySomething1)







        # FRAME RIGHT
        self.frameRight = tk.Frame(self, bg='#fcfcf7', borderwidth=3, relief="groove")
        self.frameRight.pack(side="right")
        self.frameRight.bind('<Configure>', self.resizeFrameRight)

        self.frameRight.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.frameRight.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight=1)

        self.labelFile2 = tk.Label(self.frameRight, text="File 2:", bg='#fcfcf7', borderwidth=0)
        self.textAddress2 = tk.Text(self.frameRight, state=tk.DISABLED, bg='#fcfcf7')
        self.buttonFile2 = TkinterCustomButton(master=self.frameRight)
        # Hay que crear el botón primero para poder olvidar su posición cada vez que se ajusta la ventana y sobreescribir la posición actual
        # en base a las medidas de la ventana

        self.scrollGroupsY2 = tk.Scrollbar(self.frameRight, orient=tk.VERTICAL)
        self.scrollGroupsX2 = tk.Scrollbar(self.frameRight, orient=tk.HORIZONTAL)
        self.lb2 = tk.Listbox(self.frameRight, yscrollcommand=self.scrollGroupsY2.set, xscrollcommand=self.scrollGroupsX2.set, exportselection=False)
        self.scrollGroupsY2.configure(command=self.lb2.yview)
        self.scrollGroupsX2.configure(command=self.lb2.xview)

        self.lfaddGroup2 = tk.LabelFrame(self.frameRight, text="Adding new Group", bg='#fcfcf7')
        self.lfaddGroup2.columnconfigure((0,1,2,3), weight=1)
        self.lfaddGroup2.rowconfigure((0,1,2), weight=1)
        self.labelFileNameG2 = tk.Label(self.lfaddGroup2, text="Group name:", font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textFileNameG2 = tk.Entry(self.lfaddGroup2, borderwidth=1, font=("Franklin Gothic Medium", 9), relief="solid")
        self.labelAddressG2 = tk.Label(self.lfaddGroup2, text='Address ("/" between groups):', font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textAddressG2 = tk.Entry(self.lfaddGroup2, borderwidth=1, font=("Franklin Gothic Medium", 9), relief="solid")
        self.textAddressG2.insert(0, 'Example: "/Group1/Group2"')
        self.buttonAddG2 = TkinterCustomButton(master=self.lfaddGroup2)

        self.lfDelete2 = tk.LabelFrame(self.frameRight, text="Delete dataset/group", bg='#fcfcf7')
        self.lfDelete2.columnconfigure((0,1,2,3), weight=1)
        self.lfDelete2.rowconfigure((0,1,2), weight=1)
        self.labelAddressD2 = tk.Label(self.lfDelete2, text='Address ("/" between groups):', font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textAddressD2 = tk.Entry(self.lfDelete2, borderwidth=1, font=("Franklin Gothic Medium", 9), relief="solid")
        self.textAddressD2.insert(0, 'Example: "/Group1/Group2"')
        self.buttonAddD2 = TkinterCustomButton(master=self.lfDelete2)

        self.lfmoveSomething2 = tk.LabelFrame(self.frameRight, text="Moving dataset/group", bg='#fcfcf7')
        self.lfmoveSomething2.columnconfigure((0,1,2,3), weight=1)
        self.lfmoveSomething2.rowconfigure((0,1,2,3), weight=1)
        self.labelInitAddressM2 = tk.Label(self.lfmoveSomething2, text='Init Addr ("/" between groups):', font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textInitAddressM2 = tk.Entry(self.lfmoveSomething2, borderwidth=1, relief="solid")
        self.textInitAddressM2.insert(0, 'Example: "/Group1/Group2/DatasetInit"')
        self.labelEndAddressM2 = tk.Label(self.lfmoveSomething2, text='End Addr ("/" between groups):', font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textEndAddressM2 = tk.Entry(self.lfmoveSomething2, borderwidth=1, font=("Franklin Gothic Medium", 9), relief="solid")
        self.textEndAddressM2.insert(0, 'Example: "/Group1/Group3')
        self.labelNewNameM2 = tk.Label(self.lfmoveSomething2, text="Name in new address:", font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textNewNameM2 = tk.Entry(self.lfmoveSomething2, borderwidth=1, relief="solid")
        self.buttonMove2 = TkinterCustomButton(master=self.lfmoveSomething2)

        self.lfcopySomething2 = tk.LabelFrame(self.frameRight, text="Copying dataset/group", bg='#fcfcf7')
        self.lfcopySomething2.columnconfigure((0,1,2,3), weight=1)
        self.lfcopySomething2.rowconfigure((0,1,2,3,4), weight=1)
        self.labelInitAddressC2 = tk.Label(self.lfcopySomething2, text='Init Addr ("/" between groups):', font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textInitAddressC2 = tk.Entry(self.lfcopySomething2, borderwidth=1, relief="solid")
        self.textInitAddressC2.insert(0, 'Example: "/Group1/Group2/DatasetInit"')
        self.labelEndAddressC2 = tk.Label(self.lfcopySomething2, text='End Addr ("/" between groups):', font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textEndAddressC2 = tk.Entry(self.lfcopySomething2, borderwidth=1, font=("Franklin Gothic Medium", 9), relief="solid")
        self.textEndAddressC2.insert(0, 'Example: "/Group1/Group3')
        self.labelNewNameC2 = tk.Label(self.lfcopySomething2, text="Name in new address:", font=("Franklin Gothic Medium", 9), bg='#fcfcf7', borderwidth=0)
        self.textNewNameC2 = tk.Entry(self.lfcopySomething2, borderwidth=1, relief="solid")
        self.file2To1 = tk.IntVar()
        self.buttonCheckCopy2 = tk.Checkbutton(self.lfcopySomething2, text="Copying from file 2 to 1", variable=self.file2To1, onvalue=1, offvalue=0)
        self.buttonCopy2 = TkinterCustomButton(master=self.lfcopySomething2)


    def resizeFrameLeft(self, event=0):
        self.frameLeft.pack(padx=self.winfo_width()*0.023)

        self.labelFile1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0075)))
        self.labelFile1.grid(column=0, row=0, padx=self.winfo_width()*0.01)
        self.textAddress1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.006)), width=int(self.winfo_height()*0.07), height=2)
        self.textAddress1.grid(column=1, row=0, columnspan=6, padx=self.winfo_width()*0.01)
        self.buttonFile1.grid_forget() # Borrar el button anterior y actualizarlo
        self.buttonFile1 = TkinterCustomButton(master=self.frameLeft, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=int(self.winfo_width()*0.06), height=int(self.winfo_height()*0.04), activebg_color="#f5f7d5", text_font=("Century Gothic", 8), text="Select File", text_color="#17181a",corner_radius=0, command=self.openFileFunctionLB1)
        # Se crea el botón cada vez que se ajusta la ventana para poder cambiar correctamente su tamaño
        # Esto es así puesto que no existe en la calse TkinterCustomButton un método .config para configurar su ancho y alto
        self.buttonFile1.grid(column=7, row=0, padx=int(self.winfo_width()*0.01), pady=int(self.winfo_height()*0.02))

        self.lb1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)), width=int(self.winfo_width()*0.02), height=33)
        self.lb1.grid(column=0, row=1, padx=int(self.winfo_width()*0.005), columnspan=2, rowspan=13)
        self.scrollGroupsY1.grid(column=2, row=1, sticky="NS", rowspan=13)
        self.scrollGroupsX1.grid(column=0, row=14, sticky="EW", columnspan=3)

        self.lfaddGroup1.grid(column=3, row=1, columnspan=5, rowspan=3, padx=int(self.winfo_width()*0.01))
        self.labelFileNameG1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)))
        self.labelFileNameG1.grid(column=0, row=0, sticky="NSEW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_width()*0.005))
        self.textFileNameG1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)), width=int(self.winfo_width()*0.02))
        self.textFileNameG1.grid(column=1, row=0, columnspan=3, sticky="EW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.labelAddressG1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)))
        self.labelAddressG1.grid(column=0, row=1, sticky="NSEW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.textAddressG1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)), width=int(self.winfo_width()*0.02))
        self.textAddressG1.grid(column=1, row=1, columnspan=3, sticky="EW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.buttonAddG1.grid_forget()
        self.buttonAddG1 = TkinterCustomButton(master=self.lfaddGroup1, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=int(self.winfo_width()*0.06), height=int(self.winfo_height()*0.03), activebg_color="#f5f7d5", text_font=("Century Gothic", 6), text="Add Group", text_color="#17181a", corner_radius=0, command=self.createGroupFunction1)
        self.buttonAddG1.grid(column=3, row=2, pady=int(self.winfo_width()*0.004))

        self.lfDelete1.grid(column=3, row=4, columnspan=5, rowspan=3, padx=int(self.winfo_width()*0.01), pady=int(self.winfo_height()*0.005))
        self.labelAddressD1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)))
        self.labelAddressD1.grid(column=0, row=1, sticky="NSEW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.textAddressD1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)), width=int(self.winfo_width()*0.02))
        self.textAddressD1.grid(column=1, row=1, columnspan=3, sticky="EW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.buttonAddD1.grid_forget()
        self.buttonAddD1 = TkinterCustomButton(master=self.lfDelete1, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=int(self.winfo_width()*0.06), height=int(self.winfo_height()*0.03), activebg_color="#f5f7d5", text_font=("Century Gothic", 6), text="Delete Item", text_color="#17181a", corner_radius=0, command=self.deleteFunction1)
        self.buttonAddD1.grid(column=3, row=2, pady=int(self.winfo_width()*0.004))

        self.lfmoveSomething1.grid(column=3, row=7, columnspan=5, rowspan=4, padx=int(self.winfo_width()*0.01), pady=int(self.winfo_height()*0.005))
        self.labelInitAddressM1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)))
        self.labelInitAddressM1.grid(column=0, row=0, sticky="NSEW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.textInitAddressM1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)), width=int(self.winfo_width()*0.02))
        self.textInitAddressM1.grid(column=1, row=0, columnspan=3, sticky="EW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.labelEndAddressM1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)))
        self.labelEndAddressM1.grid(column=0, row=1, sticky="NSEW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.textEndAddressM1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)), width=int(self.winfo_width()*0.02))
        self.textEndAddressM1.grid(column=1, row=1, columnspan=3, sticky="EW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.labelNewNameM1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)))
        self.labelNewNameM1.grid(column=0, row=2, sticky="NSEW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.textNewNameM1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)), width=int(self.winfo_width()*0.02))
        self.textNewNameM1.grid(column=1, row=2, columnspan=3, sticky="EW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.buttonMove1.grid_forget()
        self.buttonMove1 = TkinterCustomButton(master=self.lfmoveSomething1, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=int(self.winfo_width()*0.06), height=int(self.winfo_height()*0.03), activebg_color="#f5f7d5", text_font=("Century Gothic", 6), text="Moving Item", text_color="#17181a", corner_radius=0, command=self.movingFunction1)
        self.buttonMove1.grid(column=3, row=3, pady=int(self.winfo_width()*0.004))

        self.lfcopySomething1.grid(column=3, row=11, columnspan=5, rowspan=5, padx=int(self.winfo_width()*0.01), pady=int(self.winfo_height()*0.005))
        self.labelInitAddressC1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)))
        self.labelInitAddressC1.grid(column=0, row=0, sticky="NSEW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.textInitAddressC1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)), width=int(self.winfo_width()*0.02))
        self.textInitAddressC1.grid(column=1, row=0, columnspan=3, sticky="EW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.labelEndAddressC1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)))
        self.labelEndAddressC1.grid(column=0, row=1, sticky="NSEW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.textEndAddressC1.config(font=("Franklin Gothic Medium", int(self.winfo_width()*0.0065)), width=int(self.winfo_width()*0.02))
        self.textEndAddressC1.grid(column=1, row=1, columnspan=3, sticky="EW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.labelNewNameC1.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)))
        self.labelNewNameC1.grid(column=0, row=2, sticky="NSEW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.textNewNameC1.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)), width=int(self.winfo_width() * 0.02))
        self.textNewNameC1.grid(column=1, row=2, columnspan=3, sticky="EW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.buttonCheckCopy1.grid(column=0, row=3, columnspan=4, sticky="EW", padx=int(self.winfo_width()*0.006), pady=int(self.winfo_height()*0.005))
        self.buttonCopy1.grid_forget()
        self.buttonCopy1 = TkinterCustomButton(master=self.lfcopySomething1, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=int(self.winfo_width()*0.06), height=int(self.winfo_height()*0.03), activebg_color="#f5f7d5", text_font=("Century Gothic", 6), text="Copying Item", text_color="#17181a", corner_radius=0, command=self.copyingFunction1)
        self.buttonCopy1.grid(column=3, row=4, pady=int(self.winfo_height()*0.004))


    def resizeFrameRight(self, event=0):
        self.frameRight.pack(padx=self.winfo_width()*0.023, pady=self.winfo_width()*0.002)

        self.labelFile2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0075)))
        self.labelFile2.grid(column=0, row=0, padx=self.winfo_width() * 0.01)
        self.textAddress2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.006)), width=int(self.winfo_height() * 0.07), height=2)
        self.textAddress2.grid(column=1, row=0, columnspan=6, padx=self.winfo_width() * 0.01)
        self.buttonFile2.grid_forget()  # Borrar el button anterior y actualizarlo
        self.buttonFile2 = TkinterCustomButton(master=self.frameRight, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=int(self.winfo_width() * 0.06), height=int(self.winfo_height() * 0.04), activebg_color="#f5f7d5", text_font=("Century Gothic", 8), text="Select File", text_color="#17181a", corner_radius=0, command=self.openFileFunctionLB2)
        # Se crea el botón cada vez que se ajusta la ventana para poder cambiar correctamente su tamaño
        # Esto es así puesto que no existe en la calse TkinterCustomButton un método .config para configurar su ancho y alto
        self.buttonFile2.grid(column=7, row=0, padx=int(self.winfo_width() * 0.01), pady=int(self.winfo_height() * 0.02))

        self.lb2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)), width=int(self.winfo_width() * 0.02), height=33)
        self.lb2.grid(column=0, row=1, padx=int(self.winfo_width() * 0.005), columnspan=2, rowspan=13)
        self.scrollGroupsY2.grid(column=2, row=1, sticky="NS", rowspan=13)
        self.scrollGroupsX2.grid(column=0, row=14, sticky="EW", columnspan=3)

        self.lfaddGroup2.grid(column=3, row=1, columnspan=5, rowspan=3, padx=int(self.winfo_width() * 0.01))
        self.labelFileNameG2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)))
        self.labelFileNameG2.grid(column=0, row=0, sticky="NSEW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_width() * 0.005))
        self.textFileNameG2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)), width=int(self.winfo_width() * 0.02))
        self.textFileNameG2.grid(column=1, row=0, columnspan=3, sticky="EW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.labelAddressG2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)))
        self.labelAddressG2.grid(column=0, row=1, sticky="NSEW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.textAddressG2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)), width=int(self.winfo_width() * 0.02))
        self.textAddressG2.grid(column=1, row=1, columnspan=3, sticky="EW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.buttonAddG2.grid_forget()
        self.buttonAddG2 = TkinterCustomButton(master=self.lfaddGroup2, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=int(self.winfo_width() * 0.06), height=int(self.winfo_height() * 0.03), activebg_color="#f5f7d5", text_font=("Century Gothic", 6), text="Add Group", text_color="#17181a", corner_radius=0, command=self.createGroupFunction2)
        self.buttonAddG2.grid(column=3, row=2, pady=int(self.winfo_width() * 0.004))

        self.lfDelete2.grid(column=3, row=4, columnspan=5, rowspan=3, padx=int(self.winfo_width() * 0.01), pady=int(self.winfo_height() * 0.005))
        self.labelAddressD2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)))
        self.labelAddressD2.grid(column=0, row=1, sticky="NSEW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.textAddressD2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)), width=int(self.winfo_width() * 0.02))
        self.textAddressD2.grid(column=1, row=1, columnspan=3, sticky="EW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.buttonAddD2.grid_forget()
        self.buttonAddD2 = TkinterCustomButton(master=self.lfDelete2, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=int(self.winfo_width() * 0.06), height=int(self.winfo_height() * 0.03), activebg_color="#f5f7d5", text_font=("Century Gothic", 6), text="Delete Item", text_color="#17181a", corner_radius=0, command=self.deleteFunction2)
        self.buttonAddD2.grid(column=3, row=2, pady=int(self.winfo_width() * 0.004))

        self.lfmoveSomething2.grid(column=3, row=7, columnspan=5, rowspan=4, padx=int(self.winfo_width() * 0.01), pady=int(self.winfo_height() * 0.005))
        self.labelInitAddressM2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)))
        self.labelInitAddressM2.grid(column=0, row=0, sticky="NSEW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.textInitAddressM2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)), width=int(self.winfo_width() * 0.02))
        self.textInitAddressM2.grid(column=1, row=0, columnspan=3, sticky="EW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.labelEndAddressM2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)))
        self.labelEndAddressM2.grid(column=0, row=1, sticky="NSEW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.textEndAddressM2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)), width=int(self.winfo_width() * 0.02))
        self.textEndAddressM2.grid(column=1, row=1, columnspan=3, sticky="EW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.labelNewNameM2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)))
        self.labelNewNameM2.grid(column=0, row=2, sticky="NSEW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.textNewNameM2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)), width=int(self.winfo_width() * 0.02))
        self.textNewNameM2.grid(column=1, row=2, columnspan=3, sticky="EW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.buttonMove2.grid_forget()
        self.buttonMove2 = TkinterCustomButton(master=self.lfmoveSomething2, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=int(self.winfo_width() * 0.06), height=int(self.winfo_height() * 0.03), activebg_color="#f5f7d5", text_font=("Century Gothic", 6), text="Moving Item", text_color="#17181a", corner_radius=0, command=self.movingFunction2)
        self.buttonMove2.grid(column=3, row=3, pady=int(self.winfo_width() * 0.004))

        self.lfcopySomething2.grid(column=3, row=11, columnspan=5, rowspan=5, padx=int(self.winfo_width() * 0.01), pady=int(self.winfo_height() * 0.005))
        self.labelInitAddressC2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)))
        self.labelInitAddressC2.grid(column=0, row=0, sticky="NSEW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.textInitAddressC2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)), width=int(self.winfo_width() * 0.02))
        self.textInitAddressC2.grid(column=1, row=0, columnspan=3, sticky="EW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.labelEndAddressC2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)))
        self.labelEndAddressC2.grid(column=0, row=1, sticky="NSEW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.textEndAddressC2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)), width=int(self.winfo_width() * 0.02))
        self.textEndAddressC2.grid(column=1, row=1, columnspan=3, sticky="EW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.labelNewNameC2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)))
        self.labelNewNameC2.grid(column=0, row=2, sticky="NSEW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.textNewNameC2.config(font=("Franklin Gothic Medium", int(self.winfo_width() * 0.0065)), width=int(self.winfo_width() * 0.02))
        self.textNewNameC2.grid(column=1, row=2, columnspan=3, sticky="EW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.buttonCheckCopy2.grid(column=0, row=3, columnspan=4, sticky="EW", padx=int(self.winfo_width() * 0.006), pady=int(self.winfo_height() * 0.005))
        self.buttonCopy2.grid_forget()
        self.buttonCopy2 = TkinterCustomButton(master=self.lfcopySomething2, fg_color='#f2f7b5', border_color="#8f8989", border_width=2, width=int(self.winfo_width() * 0.06), height=int(self.winfo_height() * 0.03), activebg_color="#f5f7d5", text_font=("Century Gothic", 6), text="Copying Item",text_color="#17181a", corner_radius=0, command=self.copyingFunction2)
        self.buttonCopy2.grid(column=3, row=4, pady=int(self.winfo_height() * 0.004))


    def copyingFunction1(self):
        addressInit = self.textInitAddressC1.get()
        addressEnd = self.textEndAddressC1.get()
        addressFile = self.textAddress1.get("1.0", tk.END).strip()
        newName = self.textNewNameC1.get()
        listNotAcceptedLetters = ["'\'", "/", ":", "*", "?", '"', "<", ">", "|"]
        findInit = False
        findEnd = False
        correctName = True

        if not addressFile or not addressFile.endswith('.hdf5'):
            tk.messagebox.showinfo("Empty file", 'There is no file selected', parent=self)
        else:
            with h5py.File(addressFile, 'a') as f:
                for (path, anything) in self.h5py_iterator(f):
                    if path == addressInit.strip():
                        findInit = True
                        break

                if not findInit:
                    tk.messagebox.showinfo("Incorrect init address", "Address doesn't exists in File", parent=self)
                else:
                    if self.file1To2.get():  # Significa que se quiere copiar del fichero 1 al 2
                        addressFile2 = self.textAddress2.get("1.0", tk.END).strip()

                        if not addressFile2 or not addressFile2.endswith('.hdf5'):
                            tk.messagebox.showinfo("Empty file 2", 'There is no file selected', parent=self)
                        else:
                            with h5py.File(addressFile2, 'a') as f2:
                                for (path, anything) in self.h5py_iterator(f2):
                                    if path == addressEnd.strip():
                                        findEnd = True
                                        break

                                if not findEnd:
                                    tk.messagebox.showinfo("Incorrect end address", "Address doesn't exists in File 2", parent=self)
                                else:
                                    for letter in newName:
                                        for notAccepted in listNotAcceptedLetters:
                                            if letter == notAccepted:
                                                correctName = False
                                                break

                                    if not newName or not correctName:
                                        tk.messagebox.showinfo("Incorrect name", 'Dataset name must have characters except: \ / : * ? " < > |', parent=self)
                                    else:
                                        try:
                                            idGroup = f2.require_group(addressEnd)
                                            f.copy(addressInit, idGroup, name=newName)
                                            self.updateLB2(addressFile2)
                                        except RuntimeError:
                                            tk.messagebox.showinfo("Error", "Make sure you don´t duplicate the same item name in the same addres.", parent=self)
                                        except ValueError:
                                            tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)
                    else:
                        for (path, anything) in self.h5py_iterator(f):
                            if path == addressEnd.strip():
                                findEnd = True
                                break

                        if not findEnd:
                            tk.messagebox.showinfo("Incorrect end address", "Address doesn't exists in File", parent=self)
                        else:

                            for letter in newName:
                                for notAccepted in listNotAcceptedLetters:
                                    if letter == notAccepted:
                                        correctName = False
                                        break

                            if not newName or not correctName:
                                tk.messagebox.showinfo("Incorrect name", 'Dataset name must have characters except: \ / : * ? " < > |', parent=self)
                            else:
                                try:
                                    f.copy(addressInit, addressEnd + "/" + newName)
                                    self.updateLB1(addressFile)
                                except RuntimeError:
                                    tk.messagebox.showinfo("Error", "Make sure your end address contains the name of the moving item and the end", parent=self)
                                except ValueError:
                                    tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)

    def copyingFunction2(self):
        addressInit = self.textInitAddressC2.get()
        addressEnd = self.textEndAddressC2.get()
        addressFile = self.textAddress2.get("1.0", tk.END).strip()
        newName = self.textNewNameC2.get()
        listNotAcceptedLetters = ["'\'", "/", ":", "*", "?", '"', "<", ">", "|"]
        findInit = False
        findEnd = False
        correctName = True

        if not addressFile or not addressFile.endswith('.hdf5'):
            tk.messagebox.showinfo("Empty file", 'There is no file selected', parent=self)
        else:
            with h5py.File(addressFile, 'a') as f:
                for (path, anything) in self.h5py_iterator(f):
                    if path == addressInit.strip():
                        findInit = True
                        break

                if not findInit:
                    tk.messagebox.showinfo("Incorrect init address", "Address doesn't exists in File", parent=self)
                else:
                    if self.file2To1.get():  # Significa que se quiere copiar del fichero 1 al 2
                        addressFile1 = self.textAddress1.get("1.0", tk.END).strip()

                        if not addressFile1 or not addressFile1.endswith('.hdf5'):
                            tk.messagebox.showinfo("Empty file 1", 'There is no file selected', parent=self)
                        else:
                            with h5py.File(addressFile1, 'a') as f2:
                                for (path, anything) in self.h5py_iterator(f2):
                                    if path == addressEnd.strip():
                                        findEnd = True
                                        break

                                if not findEnd:
                                    tk.messagebox.showinfo("Incorrect end address", "Address doesn't exists in File 1", parent=self)
                                else:
                                    for letter in newName:
                                        for notAccepted in listNotAcceptedLetters:
                                            if letter == notAccepted:
                                                correctName = False
                                                break

                                    if not newName or not correctName:
                                        tk.messagebox.showinfo("Incorrect name", 'Dataset name must have characters except: \ / : * ? " < > |', parent=self)
                                    else:
                                        try:
                                            idGroup = f2.require_group(addressEnd)
                                            f.copy(addressInit, idGroup, name=newName)
                                            self.updateLB1(addressFile)
                                        except RuntimeError:
                                            tk.messagebox.showinfo("Error", "Make sure you don´t duplicate the same item name in the same addres.", parent=self)
                                        except ValueError:
                                            tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)
                    else:

                        for (path, anything) in self.h5py_iterator(f):
                            if path == addressEnd.strip():
                                findEnd = True
                                break

                        if not findEnd:
                            tk.messagebox.showinfo("Incorrect end address", "Address doesn't exists in File 2", parent=self)
                        else:

                            for letter in newName:
                                for notAccepted in listNotAcceptedLetters:
                                    if letter == notAccepted:
                                        correctName = False
                                        break

                            if not newName or not correctName:
                                tk.messagebox.showinfo("Incorrect name", 'Dataset name must have characters except: \ / : * ? " < > |', parent=self)
                            else:
                                try:
                                    f.copy(addressInit, addressEnd + "/" + newName)
                                    self.updateLB2(addressFile)
                                except RuntimeError:
                                    tk.messagebox.showinfo("Error", "Make sure your end address contains the name of the moving item and the end", parent=self)
                                except ValueError:
                                    tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)


    def movingFunction1(self):
        addressInit = self.textInitAddressM1.get()
        addressEnd = self.textEndAddressM1.get()
        addressFile = self.textAddress1.get("1.0", tk.END).strip()
        newName = self.textNewNameM1.get()
        listNotAcceptedLetters = ["'\'", "/", ":", "*", "?", '"', "<", ">", "|"]
        findInit = False
        findEnd = False
        correctName = True

        if not addressFile:
            tk.messagebox.showinfo("Empty file 1", 'There is no file selected', parent=self)
        else:
            with h5py.File(addressFile, 'a') as f:
                for (path, anything) in self.h5py_iterator(f):
                    if path == addressInit.strip():
                        findInit = True
                        break

                if not findInit:
                    tk.messagebox.showinfo("Incorrect init address", "Address doesn't exists in File", parent=self)
                else:

                    for (path, anything) in self.h5py_iterator(f):
                        if path == addressEnd.strip():
                            findEnd = True
                            break

                    if not findEnd:
                        tk.messagebox.showinfo("Incorrect end address", "Address doesn't exists in File", parent=self)
                    else:

                        for letter in newName:
                            for notAccepted in listNotAcceptedLetters:
                                if letter == notAccepted:
                                    correctName = False
                                    break

                        if not newName or not correctName:
                            tk.messagebox.showinfo("Incorrect name", 'Dataset name must have characters except: \ / : * ? " < > |', parent=self)
                        else:
                            try:
                                f.move(addressInit, addressEnd + "/" + newName)
                                self.updateLB1(addressFile)
                            except ValueError:
                                tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)

    def movingFunction2(self):
        addressInit = self.textInitAddressM2.get()
        addressEnd = self.textEndAddressM2.get()
        addressFile = self.textAddress2.get("1.0", tk.END).strip()
        newName = self.textNewNameM2.get()
        listNotAcceptedLetters = ["'\'", "/", ":", "*", "?", '"', "<", ">", "|"]
        findInit = False
        findEnd = False
        correctName = True

        if not addressFile:
            tk.messagebox.showinfo("Empty file", 'There is no file selected', parent=self)
        else:
            with h5py.File(addressFile, 'a') as f:
                for (path, anything) in self.h5py_iterator(f):
                    if path == addressInit.strip():
                        findInit = True
                        break

                if not findInit:
                    tk.messagebox.showinfo("Incorrect init address", "Address doesn't exists in File", parent=self)
                else:

                    for (path, anything) in self.h5py_iterator(f):
                        if path == addressEnd.strip():
                            findEnd = True
                            break

                    if not findEnd:
                        tk.messagebox.showinfo("Incorrect end address", "Address doesn't exists in File", parent=self)
                    else:

                        for letter in newName:
                            for notAccepted in listNotAcceptedLetters:
                                if letter == notAccepted:
                                    correctName = False
                                    break

                        if not newName or not correctName:
                            tk.messagebox.showinfo("Incorrect name", 'Dataset name must have characters except: \ / : * ? " < > |', parent=self)
                        else:
                            try:
                                f.move(addressInit, addressEnd + "/" + newName)
                                self.updateLB2(addressFile)
                            except ValueError:
                                tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)

    def deleteFunction1(self):
        addressDel = self.textAddressD1.get()
        addressFile = self.textAddress1.get("1.0", tk.END).strip()
        find = False

        if not addressFile:
            tk.messagebox.showinfo("Empty file", 'There is no file selected', parent=self)
        else:
            with h5py.File(addressFile, 'a') as f:
                for (path, anything) in self.h5py_iterator(f):
                    if path == addressDel.strip():
                        find = True
                        break

                if not find:
                    tk.messagebox.showinfo("Incorrect address", "Address doesn't exists in File", parent=self)
                else:
                    del f[path]
                    self.updateLB1(addressFile)

    def deleteFunction2(self):
        addressDel = self.textAddressD2.get()
        addressFile = self.textAddress2.get("1.0", tk.END).strip()
        find = False

        if not addressFile:
            tk.messagebox.showinfo("Empty file", 'There is no file selected', parent=self)
        else:
            with h5py.File(addressFile, 'a') as f:
                for (path, anything) in self.h5py_iterator(f):
                    if path == addressDel.strip():
                        find = True
                        break

                if not find:
                    tk.messagebox.showinfo("Incorrect address", "Address doesn't exists in File", parent=self)
                else:
                    del f[path]
                    self.updateLB2(addressFile)


    def createGroupFunction1(self):
        find = False
        correctName = True
        listNotAcceptedLetters = ["'\'", "/", ":", "*", "?", '"', "<", ">", "|"]
        nameG = self.textFileNameG1.get()
        addressG = self.textAddressG1.get()
        addressFile = self.textAddress1.get("1.0", tk.END).strip()

        if not addressFile:
            tk.messagebox.showinfo("Empty file", 'There is no file selected', parent=self)
        else:
            for letter in nameG:
                for notAccepted in listNotAcceptedLetters:
                    if letter == notAccepted:
                        correctName = False
                        break

            if not nameG or not correctName:
                tk.messagebox.showinfo("Incorrect name", 'Group name must have characters except: \ / : * ? " < > |', parent=self)
            else:
                with h5py.File(addressFile, 'r+') as f:

                    if addressG != "/":
                        for (path, anything) in self.h5py_iterator(f):
                            if path == addressG.strip():
                                find = True
                                break
                    else:
                        find = True

                    if not find:
                        tk.messagebox.showinfo("Incorrect address", "Address doesn't exists in File", parent=self)
                    else:
                        try:
                            f.create_group(addressG.strip()[1:len(addressG.strip())] + "/" + nameG)
                            self.updateLB1(addressFile)
                        except ValueError:
                            tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)



    def createGroupFunction2(self):
        find = False
        correctName = True
        listNotAcceptedLetters = ["'\'", "/", ":", "*", "?", '"', "<", ">", "|"]
        nameG = self.textFileNameG2.get()
        addressG = self.textAddressG2.get()
        addressFile = self.textAddress2.get("1.0", tk.END).strip()

        if not addressFile:
            tk.messagebox.showinfo("Empty file", 'There is no file selected', parent=self)
        else:
            for letter in nameG:
                for notAccepted in listNotAcceptedLetters:
                    if letter == notAccepted:
                        correctName = False
                        break

            if not nameG or not correctName:
                tk.messagebox.showinfo("Incorrect name", 'Group name must have characters except: \ / : * ? " < > |', parent=self)
            else:
                with h5py.File(addressFile, 'r+') as f:

                    if addressG != "/":
                        for (path, anything) in self.h5py_iterator(f):
                            if path == addressG.strip():
                                find = True
                                break
                    else:
                        find = True

                    if not find:
                        tk.messagebox.showinfo("Incorrect address", "Address doesn't exists in File", parent=self)
                    else:
                        try:
                            f.create_group(addressG.strip()[1:len(addressG.strip())] + "/" + nameG)
                            self.updateLB2(addressFile)
                        except ValueError:
                            tk.messagebox.showinfo("Error", "Make sure the name is not repeated in the same address.", parent=self)



    def updateLB1(self, addressFile):
        with h5py.File(addressFile, 'r+') as f:
            self.lb1.delete(0, tk.END)
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
                    self.lb1.insert(tk.END, "   " + numSpace + "\u2501 " + pathFinal)
                elif anythingFinal == "dataset":
                    self.lb1.insert(tk.END, "   " + numSpace + "\u2022 " + pathFinal)

    def updateLB2(self, addressFile):
        with h5py.File(addressFile, 'r+') as f:
            self.lb2.delete(0, tk.END)
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
                    self.lb2.insert(tk.END, "   " + numSpace + "\u2501 " + pathFinal)
                elif anythingFinal == "dataset":
                    self.lb2.insert(tk.END, "   " + numSpace + "\u2022 " + pathFinal)

    def openFileFunctionLB1(self):
        file = filedialog.askopenfilename(title="Choose a HDF5 file", filetypes=(("*.hdf5", "*.hdf5"), ("All Files (*.*)", "*.*")))
        self.textAddress1.config(state=tk.NORMAL)
        self.textAddress1.delete('1.0', tk.END)
        self.textAddress1.insert('1.0', file)
        self.textAddress1.config(state=tk.DISABLED)

        if not file.endswith('.hdf5'):
            self.lb1.delete(0, tk.END)
            self.lb1.insert(tk.END, "\n\n\n\t\t     FILE HAS NOT HDF5 EXTENSION")
        else:
            self.updateLB1(file)
        self.focus_force()

    def openFileFunctionLB2(self):
        file = filedialog.askopenfilename(title="Choose a HDF5 file", filetypes=(("*.hdf5", "*.hdf5"), ("All Files (*.*)", "*.*")))
        self.textAddress2.config(state=tk.NORMAL)
        self.textAddress2.delete('1.0', tk.END)
        self.textAddress2.insert('1.0', file)
        self.textAddress2.config(state=tk.DISABLED)

        if not file.endswith('.hdf5'):
            self.lb2.delete(0, tk.END)
            self.lb2.insert(tk.END, "\n\n\n\t\t     FILE HAS NOT HDF5 EXTENSION")
        else:
            self.updateLB2(file)
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

    def resizeFrameTop(self, event=0):
        self.labelTop.pack(side="left", padx=self.winfo_width()*0.035, pady=self.winfo_height()*0.02)
        self.labelISATI.pack(side="left", padx=self.winfo_width()*0.17)
        self.buttonExit.pack(side="right", padx=self.winfo_width()*0.02)
