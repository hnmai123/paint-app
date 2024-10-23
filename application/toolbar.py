import tkinter as tk
from tkinter import colorchooser
from tkmacosx import Button

class Toolbar(tk.Frame):
    def __init__(self, master=None, 
                 set_color=None, 
                 clear_space=None, 
                 set_eraser=None,                  
                 set_shape=None,
                 normal_drawing=None):
        super().__init__(master)

        self.master = master
        self.set_color = set_color
        self.clear_space = clear_space
        self.set_eraser = set_eraser
        self.set_shape = set_shape
        self.shapes = ["Line", "Rectangle", "Circle"]
        self.selected_shape = tk.StringVar(value=None)
        self.color = "black"
        self.normal_drawing = normal_drawing
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.color_button = Button(self, bg="black", width=50, height=50, borderless=True, activebackground="black", command=self.choose_color, borderwidth=0)
        self.color_button.grid(row=0, column=0, padx=5)

        self.eraser = tk.PhotoImage(file="assets/eraser.png").subsample(14)
        self.eraser_button = tk.Button(self, image=self.eraser, command=self.erase_mode)
        self.eraser_button.grid(row=0, column=1, padx=5)

        self.pen = tk.PhotoImage(file="assets/pencil.png").subsample(14)
        self.pen_button = tk.Button(self, image=self.pen, command=self.normal_mode)
        self.pen_button.grid(row=0, column=3, padx=5)

        self.shapes_image = {
            "Line": tk.PhotoImage(file="assets/line.png").subsample(14),
            "Rectangle": tk.PhotoImage(file="assets/rectangle.png").subsample(14),
            "Circle": tk.PhotoImage(file="assets/circle.png").subsample(14)
        }
        self.shapes_icon = tk.PhotoImage(file="assets/shapes.png").subsample(14)
        self.shapes_menu = tk.Menubutton(self, image=self.shapes_icon, indicatoron=True, borderwidth=1, relief="raised")
        self.menu = tk.Menu(self.shapes_menu, tearoff=False)
        self.shapes_menu.configure(menu=self.menu)

        for shape in self.shapes:
            self.menu.add_radiobutton(label=shape, 
                                      variable=self.selected_shape, 
                                      value=shape, 
                                      image=self.shapes_image[shape], 
                                      compound="left", 
                                      command=self.shape_mode)
        
        self.shapes_menu.grid(row=0, column=4, padx=5)
        self.clear_button = tk.Button(self, text="Clear", command=self.reset_clear_space)
        self.clear_button.grid(row=0, column=7, padx=5)

    def choose_color(self, color = "black"):
        color = colorchooser.askcolor(title="Choose a color")
        if color:
            self.color_button.configure(background=str(color[1]), activebackground=str(color[1]))
            self.set_color(color[1])
        self.color = color[1]

    def shape_mode(self):
        selected_shape = self.selected_shape.get()
        if selected_shape:  # Only update if a shape is selected
            self.shapes_menu.config(image=self.shapes_image[selected_shape])
            self.set_shape(selected_shape)
        self.set_color(self.color)

    def normal_mode(self):
        self.normal_drawing()
        self.shapes_menu.config(image=self.shapes_icon)
        self.set_shape(None)
        self.selected_shape.set(None)  # Clear the selection of the shape
        self.set_color(self.color)
        
    def reset_clear_space(self):
        self.clear_space()
        self.color_button.configure(background="black", activebackground="black")
        self.shapes_menu.config(image=self.shapes_icon)
        self.set_shape(None)
        self.selected_shape.set(None)  # Clear the selection of the shape
        self.color = "black"
        
    def erase_mode(self):
        self.set_eraser()
        self.set_shape(None)
        self.selected_shape.set(None)  # Clear the selection of the shape
        self.shapes_menu.config(image=self.shapes_icon)