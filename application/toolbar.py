import tkinter as tk
from tkinter import colorchooser

class Toolbar(tk.Frame):
    def __init__(self, master=None, 
                 set_color=None, 
                 clear_space=None, 
                 set_eraser=None, 
                 set_shape=None,
                 normal_drawing=None,
                 set_brush_size=None):
        super().__init__(master)

        self.master = master
        self.set_color = set_color
        self.clear_space = clear_space
        self.set_eraser = set_eraser
        self.set_shape = set_shape
        self.color = "black"
        self.shapes = ["Line", "Rectangle", "Circle"]
        self.selected_shape = tk.StringVar(value=None)
        self.normal_drawing = normal_drawing
        self.set_brush_size = set_brush_size
        self.default_brush_size = 5
        self.brush_size = self.default_brush_size
        self.erase_size = 50

        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.color_image = tk.PhotoImage(file="assets/colour.png").subsample(14)
        self.color_button = tk.Button(self, image=self.color_image, command=self.choose_color)
        self.color_button.grid(row=0, column=0, padx=5)

        self.color_label = tk.Label(self, bg="black", width=4, height = 2, relief="sunken")
        self.color_label.grid(row=0, column=1, padx=5)

        # Eraser button
        self.eraser = tk.PhotoImage(file="assets/eraser.png").subsample(14)
        self.eraser_button = tk.Button(self, image=self.eraser, command=self.erase_mode)
        self.eraser_button.grid(row=0, column=2, padx=5)

        # Pen button
        self.pen = tk.PhotoImage(file="assets/pencil.png").subsample(14)
        self.pen_button = tk.Button(self, image=self.pen, command=self.normal_mode)
        self.pen_button.grid(row=0, column=3, padx=5)

        # Shapes menu
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


        # Brush size button
        self.bursh_image = tk.PhotoImage(file="assets/brush.png").subsample(14)
        self.brush_button = tk.Button(self, image=self.bursh_image, command=self.display_brush_slider)
        self.brush_button.grid(row=0, column=5, padx=5)

        # Brush size slider
        self.brush_size_slider = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL, label="Brush Size",
                                          command=self.update_brush_size)
        self.brush_size_slider.set(self.default_brush_size)  # Default brush size
        self.brush_size_slider.grid(row=0, column=5, padx=5)
        self.brush_size_slider.grid_remove()

        # Clear button
        self.clear_button = tk.Button(self, text="Clear", command=self.reset_clear_space)
        self.clear_button.grid(row=0, column=7, padx=5)

    def choose_color(self, color = "black"):
        color = colorchooser.askcolor(title="Choose a color")
        if color:
            self.color_label.config(background=str(color[1]))
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
        self.brush_size_slider.set(self.default_brush_size)

    def reset_clear_space(self):
        self.clear_space()
        self.color_label.config(background="black")
        self.shapes_menu.config(image=self.shapes_icon)
        self.set_shape(None)
        self.selected_shape.set(None)  # Clear the selection of the shape
        self.color = "black"
        self.brush_size_slider.set(self.default_brush_size)

    def erase_mode(self):
        self.set_eraser()
        self.set_shape(None)
        self.selected_shape.set(None)  # Clear the selection of the shape
        self.shapes_menu.config(image=self.shapes_icon)
        self.brush_size_slider.set(self.erase_size)

    def display_brush_slider(self):
        self.brush_size_slider.grid()

    def update_brush_size(self, size):
        self.brush_size = int(size)
        self.set_brush_size(self.brush_size)
