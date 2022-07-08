import tkinter
import sys


class TkinterCustomButton(tkinter.Frame):
    """ tkinter custom button with border, rounded corners and hover effect

        Arguments:  master= where to place button
                    bg_color= background color, None is standard,
                    fg_color= foreground color, blue is standard,
                    hover_color= foreground color, lightblue is standard,
                    border_color= foreground color, None is standard,
                    border_width= border thickness, 0 is standard,
                    command= callback function, None is standard,
                    width= width of button, 110 is standard,
                    height= width of button, 35 is standard,
                    corner_radius= corner radius, 10 is standard,
                    text_font= (<Name>, <Size>),
                    text_color= text color, white is standard,
                    text= text of button,
                    hover= hover effect, True is standard,
                    image= PIL.PhotoImage, standard is None"""

    def __init__(self,
                 bg_color=None,
                 activebg_color=None,
                 fg_color="#2874A6",
                 hover_color=None,
                 border_color=None,
                 border_width=0,
                 command=None,
                 width=120,
                 height=40,
                 corner_radius=10,
                 text_font=None,
                 text_color="white",
                 text="CustomButton",
                 hover=False,
                 image=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        if bg_color is None:
            self.bg_color = self.master.cget("bg")
        else:
            self.bg_color = bg_color

        self.fg_color = fg_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.activebg_color = activebg_color

        self.width = width
        self.height = height

        if corner_radius*2 > self.height:
            self.corner_radius = self.height/2
        elif corner_radius*2 > self.width:
            self.corner_radius = self.width/2
        else:
            self.corner_radius = corner_radius

        self.border_width = border_width

        if self.corner_radius >= self.border_width:
            self.inner_corner_radius = self.corner_radius - self.border_width
        else:
            self.inner_corner_radius = 0

        self.text = text
        self.text_color = text_color
        if text_font is None:
            if sys.platform == "darwin":  # macOS
                self.text_font = ("Avenir", 13)
            elif "win" in sys.platform:  # Windows
                self.text_font = ("Century Gothic", 11)
            else:
                self.text_font = ("TkDefaultFont")
        else:
            self.text_font = text_font

        self.image = image

        self.function = command
        self.hover = hover

        self.configure(width=self.width, height=self.height)

        if self.function is not None:
            self.configure(cursor="hand2")

        self.canvas = tkinter.Canvas(master=self, highlightthicknes=0, background=self.bg_color, width=self.width, height=self.height)
        self.canvas.place(x=0, y=0)

        if self.hover is True:
            self.canvas.bind("<Enter>", self.on_enter)
            self.canvas.bind("<Leave>", self.on_leave)

        self.canvas.bind("<ButtonPress>", self.on_press)
        self.canvas.bind("<ButtonRelease>", self.on_release)

        self.canvas_fg_parts = []
        self.canvas_border_parts = []
        self.text_part = None
        self.text_label = None
        self.image_label = None

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.canvas_fg_parts = []
        self.canvas_border_parts = []
        self.canvas.configure(bg=self.bg_color)

        # border button parts
        if self.border_width > 0:

            if self.corner_radius > 0:
                self.canvas_border_parts.append(self.canvas.create_oval(0, 0, self.corner_radius * 2, self.corner_radius * 2))
                self.canvas_border_parts.append(self.canvas.create_oval(self.width - self.corner_radius * 2, 0, self.width, self.corner_radius * 2))
                self.canvas_border_parts.append(self.canvas.create_oval(0, self.height - self.corner_radius * 2, self.corner_radius * 2, self.height))
                self.canvas_border_parts.append(self.canvas.create_oval(self.width - self.corner_radius * 2, self.height - self.corner_radius * 2, self.width, self.height))

            self.canvas_border_parts.append(self.canvas.create_rectangle(0, self.corner_radius, self.width, self.height - self.corner_radius))
            self.canvas_border_parts.append(self.canvas.create_rectangle(self.corner_radius, 0, self.width - self.corner_radius, self.height))

        # inner button parts

        if self.corner_radius > 0:
            self.canvas_fg_parts.append(self.canvas.create_oval(self.border_width, self.border_width,  self.border_width + self.inner_corner_radius * 2, self.border_width + self.inner_corner_radius * 2))
            self.canvas_fg_parts.append(self.canvas.create_oval(self.width - self.border_width - self.inner_corner_radius * 2, self.border_width, self.width - self.border_width, self.border_width + self.inner_corner_radius * 2))
            self.canvas_fg_parts.append(self.canvas.create_oval(self.border_width, self.height - self.border_width - self.inner_corner_radius * 2, self.border_width + self.inner_corner_radius * 2, self.height-self.border_width))
            self.canvas_fg_parts.append(self.canvas.create_oval(self.width - self.border_width - self.inner_corner_radius * 2, self.height - self.border_width - self.inner_corner_radius * 2,self.width - self.border_width, self.height - self.border_width))

        self.canvas_fg_parts.append(self.canvas.create_rectangle(self.border_width + self.inner_corner_radius, self.border_width, self.width - self.border_width - self.inner_corner_radius, self.height - self.border_width))
        self.canvas_fg_parts.append(self.canvas.create_rectangle(self.border_width, self.border_width + self.inner_corner_radius, self.width - self.border_width, self.height - self.inner_corner_radius - self.border_width))

        for part in self.canvas_fg_parts:
            self.canvas.itemconfig(part, fill=self.fg_color, width=0)

        for part in self.canvas_border_parts:
            self.canvas.itemconfig(part, fill=self.border_color, width=0)

        # no image given
        if self.image is None:
            # create tkinter.Label with text
            self.text_label = tkinter.Label(master=self, text=self.text, font=self.text_font, bg=self.fg_color, fg=self.text_color)
            self.text_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            self.text_label.bind("<ButtonPress>", self.on_press)
            self.text_label.bind("<ButtonRelease>", self.on_release)

            self.set_text(self.text)

        # use the given image
        else:
            # create tkinter.Label with image on it
            self.image_label = tkinter.Label(master=self, image=self.image, bg=self.fg_color)
            self.image_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            self.image_label.bind("<ButtonPress>", self.on_press)
            self.image_label.bind("<ButtonRelease>", self.on_release)


    def set_text(self, text):
        if self.text_label is not None:
            self.text_label.configure(text=text)


    def on_enter(self, event=0):
        for part in self.canvas_fg_parts:
            self.canvas.itemconfig(part, fill=self.hover_color, width=0)

        if self.text_label is not None:
            # change background color of image_label
            self.text_label.configure(bg=self.hover_color)

        if self.image_label is not None:
            # change background color of image_label
            self.image_label.configure(bg=self.hover_color)


    def on_leave(self, event=0):
        for part in self.canvas_fg_parts:
            self.canvas.itemconfig(part, fill=self.fg_color, width=0)

        if self.text_label is not None:
            # change background color of image_label
            self.text_label.configure(bg=self.fg_color)

        if self.image_label is not None:
            # change background color of image_label
            self.image_label.configure(bg=self.fg_color)


    def on_press(self, event=0):
        for part in self.canvas_fg_parts:
            self.canvas.itemconfig(part, fill=self.activebg_color, width=0)

        if self.text_label is not None:
            # change background color of image_label
            self.text_label.configure(bg=self.activebg_color)

        if self.image_label is not None:
            # change background color of image_label
            self.image_label.configure(bg=self.activebg_color)


    def on_release(self, event=0):
        self.on_leave()
        if self.function is not None:
            self.function()


