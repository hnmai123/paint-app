import tkinter as tk
from tkinter import colorchooser

# Tpppbar class inherits from tk.Frame and provide various tools (color, shape, size, etc.) to draw on the canvas
class Toolbar(tk.Frame):
    def __init__(self, master=None, 
                 set_color=None, 
                 clear_space=None, 
                 set_eraser=None, 
                 set_shape=None,
                 normal_drawing=None,
                 set_brush_size=None,
                 set_fill_mode=None,
                 open_image=None,
                 save_image=None,
                 undo=None,
                 redo=None):
        super().__init__(master)

        # Initialize the toolbar with the callback functions for the drawing actions
        self.master = master
        self.set_color = set_color # Set the color function
        self.clear_space = clear_space # Clear the drawing space function
        self.set_eraser = set_eraser # Set the eraser function
        self.set_shape = set_shape  # Set the shape function
        self.color = "black" # Default color
        self.shapes = ["Line", "Rectangle", "Circle"] # Available shapes
        self.selected_shape = tk.StringVar(value=None) # Selected shape
        self.normal_drawing = normal_drawing # Set the normal drawing mode function
        self.set_brush_size = set_brush_size  # Set the brush size function
        self.default_brush_size = 5
        self.brush_size = self.default_brush_size
        self.erase_size = 50 # Default eraser size
        self.set_fill_mode = set_fill_mode # Set the fill mode function
        self.open_image = open_image # Open image function
        self.save_image = save_image # Save image function
        self.undo = undo # Undo function
        self.redo = redo # Redo function
        self.create_widgets() # Create toolbar buttons
        self.pack()

    # Create toolbar buttons and menu options
    def create_widgets(self):
        # Color selections button
        self.color_image = tk.PhotoImage(file="assets/colour.png").subsample(14)
        self.color_button = tk.Button(self, image=self.color_image, command=self.choose_color, text="Color", compound="top")
        self.color_button.grid(row=0, column=0, padx=5)

        # Display chosen color and button to change color
        self.color_label = tk.Button(self, bg="black", width=4, height = 3, relief="sunken", command=self.choose_color)
        self.color_label.grid(row=0, column=1, padx=5)

        # Eraser button
        self.eraser = tk.PhotoImage(file="assets/eraser.png").subsample(14)
        self.eraser_button = tk.Button(self, image=self.eraser, command=self.erase_mode, text="Erase", compound="top")
        self.eraser_button.grid(row=0, column=2, padx=5)

        # Pen button for normal drawing mode
        self.pen = tk.PhotoImage(file="assets/pencil.png").subsample(14)
        self.pen_button = tk.Button(self, image=self.pen, command=self.normal_mode, text="Draw", compound="top")
        self.pen_button.grid(row=0, column=3, padx=5)

        # Shapes menu for shapes selection
        self.shapes_image = {
            "Line": tk.PhotoImage(file="assets/line.png").subsample(14),
            "Rectangle": tk.PhotoImage(file="assets/rectangle.png").subsample(14),
            "Circle": tk.PhotoImage(file="assets/circle.png").subsample(14)
        }
        # Shapes menu
        self.shapes_icon = tk.PhotoImage(file="assets/shapes.png").subsample(14)
        self.shapes_menu = tk.Menubutton(self, image=self.shapes_icon, indicatoron=True, borderwidth=1, relief="raised", text="Shapes", compound="top", pady=5)
        self.menu = tk.Menu(self.shapes_menu, tearoff=False)
        self.shapes_menu.configure(menu=self.menu)
        # Add shape options to the menu
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
        self.brush_button = tk.Button(self, image=self.bursh_image, command=self.display_brush_slider, text="Size", compound="top")
        self.brush_button.grid(row=0, column=5, padx=5)

        # Slider for adjusting the brush size
        self.brush_size_slider = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL, label="Brush Size",
                                          command=self.update_brush_size)
        self.brush_size_slider.set(self.default_brush_size)  # Default brush size
        self.brush_size_slider.grid(row=0, column=5, padx=5)
        self.brush_size_slider.grid_remove()

        # Fill color button
        self.color_bucket_image = tk.PhotoImage(file="assets/paint-bucket.png").subsample(14)
        self.color_bucket_button = tk.Button(self, image=self.color_bucket_image, command=self.fill_mode, text="Fill", compound="top")
        self.color_bucket_button.grid(row=0, column=6, padx=5)

        # Undo button
        self.undo_image = tk.PhotoImage(file="assets/undo.png").subsample(14)
        self.undo_button = tk.Button(self, image=self.undo_image, command=self.undo, text="Undo", compound="top")
        self.undo_button.grid(row=0, column=7, padx=5)

        # Redo button
        self.redo_image = tk.PhotoImage(file="assets/redo.png").subsample(14)
        self.redo_button = tk.Button(self, image=self.redo_image, command=self.redo, text="Redo", compound="top")
        self.redo_button.grid(row=0, column=8, padx=5)

        # Clear button
        self.clear_button = tk.Button(self, text="Clear", command=self.reset_clear_space)
        self.clear_button.grid(row=0, column=9, padx=5)

        # Open button
        self.open_button = tk.Button(self, text="Open", command=self.open_image)
        self.open_button.grid(row=0, column=10, padx=5)

        # Save button
        self.save_button = tk.Button(self, text="Save", command=self.save_image)
        self.save_button.grid(row=0, column=11, padx=5)

    # Function to open color chooser dialog and set chosen color
    def choose_color(self, color = "black"):
        color = colorchooser.askcolor(title="Choose a color")
        if color:
            self.color_label.config(background=str(color[1]))
            self.set_color(color[1])
            self.color = color[1]
        self.update_brush_size(self.brush_size) # Ensure brush size is updated

    # Function to set the selected shape mode
    def shape_mode(self):
        selected_shape = self.selected_shape.get()
        if selected_shape:  # Only update if a shape is selected
            self.shapes_menu.config(image=self.shapes_image[selected_shape])
            self.set_shape(selected_shape)
        self.set_color(self.color)
        self.brush_size_slider.set(self.brush_size)
        self.update_brush_size(self.brush_size) # Ensure brush size is updated

    # Function to set the normal drawing mode
    def normal_mode(self):
        self.normal_drawing()
        self.shapes_menu.config(image=self.shapes_icon)
        self.set_shape(None)
        self.selected_shape.set(None)  # Clear the selection of the shape
        self.set_color(self.color) # Set color after selecting shape mode
        self.brush_size_slider.set(self.brush_size)
        self.update_brush_size(self.brush_size) # Ensure brush size is updated

    # Function to reset the drawing space and set the default color and shape
    def reset_clear_space(self):
        self.clear_space()
        self.color_label.config(background="black")
        self.shapes_menu.config(image=self.shapes_icon)
        self.set_shape(None) # Set the shape to None
        self.selected_shape.set(None)  # Clear the selection of the shape
        self.color = "black" # Reset the color to black (default)
        self.brush_size_slider.set(self.default_brush_size) # Reset the brush size
        self.brush_size_slider.grid_remove()

    # Function to set the eraser mode
    def erase_mode(self):
        self.set_shape(None)
        self.selected_shape.set(None)  # Clear the selection of the shape
        self.shapes_menu.config(image=self.shapes_icon)
        self.brush_size_slider.set(self.erase_size)
        self.brush_size_slider.grid_remove()
        self.set_eraser()

    # Function to display the brush size slider
    def display_brush_slider(self):
        self.brush_size_slider.grid()

    # Function to update the brush size
    def update_brush_size(self, size):
        self.brush_size = int(size)
        self.set_brush_size(self.brush_size)

    # Function to set the fill mode
    def fill_mode(self):
        self.set_shape(None)
        self.selected_shape.set(None)
        self.shapes_menu.config(image=self.shapes_icon)
        self.brush_size_slider.set(self.brush_size)
        self.update_brush_size(self.brush_size) # Ensure brush size is updated
        self.set_fill_mode()
