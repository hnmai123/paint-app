import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk

# Drawing class inherits from tk.Canvas and provides the drawing functionality
class Drawing(tk.Canvas):
    def __init__(self, master=None, width =None, height = None, background = None):
        super().__init__(master, width = width, height = height, background=background)
        self.master = master
        self.configure(cursor="@assets/pencil.xbm") # Set the initial cursor to pencil
        self.old_x = None
        self.old_y = None
        self.default_pen_color = "black"    
        self.pen_color = self.default_pen_color  # Set initial pen color to black
        self.default_line_width = 5
        self.erase_default_line_width = 50
        self.line_width = self.default_line_width
        self.shape = None
        self.eraser_mode = False
        self.fill_mode = False

        # Create a PIL image for drawing and saving
        self.image = Image.new("RGB", (width, height), background) # Create a new image
        self.draw = ImageDraw.Draw(self.image) # Create a drawing object

        # Stacks to store states for undo and redo functionality
        self.undo_stack = []
        self.redo_stack = []

        # Bind the mouse events to the drawing functions
        self.bind('<Button-1>', self.activate_paint)
        self.bind('<B1-Motion>', self.paint)
        self.bind('<ButtonRelease-1>', self.reset)
        self.bind('<Motion>', self.track_mouse)

        self.save_state() # Save the first initial state for undo and redo functionality

    def activate_paint(self, event):
        # If in fill mode, fill the clicked area; else, start drawing
        if self.fill_mode:
            self.fill_area(event.x, event.y)
        else:
            self.old_x = event.x
            self.old_y = event.y            
            # Draw different shapes based on self.shape selection
            if self.shape == "Line":
                self.temp_shape = self.create_line(self.old_x, self.old_y, event.x, event.y, fill=self.pen_color, width=self.line_width)
            elif self.shape == "Rectangle":
                self.temp_shape = self.create_rectangle(self.old_x, self.old_y, event.x, event.y, outline=self.pen_color, width=self.line_width)
            elif self.shape == "Circle":
                self.temp_shape = self.create_oval(self.old_x, self.old_y, event.x, event.y, outline=self.pen_color, width=self.line_width)
            elif not self.eraser_mode:
                # Draw point for freehand drawing
                self.create_oval(event.x - self.line_width / 2, event.y - self.line_width / 2,
                                event.x + self.line_width / 2, event.y + self.line_width / 2,
                                fill=self.pen_color, outline=self.pen_color)

    # Function to save the current state of the drawing
    def save_state(self):
        self.delete("mouse_cursor") # Remove cursor preview before saving
        ps_file = "state_canvas.ps" # Postscript file for saving the state
        self.postscript(file=ps_file, colormode='color') # Save the current state to the postscript file
        img = Image.open(ps_file).copy() # Open the saved postscript file and get a copy of the image
        self.undo_stack.append(img) # Push the image to the undo stack
        self.redo_stack.clear() # Clear the redo stack on new actions

    # Function to undo the last action
    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.image.copy()) # Push the current state to the redo stack
            last_action = self.undo_stack.pop() # Pop the last action from the undo stack
            self.image = last_action # Set the image to the last action
            self.draw = ImageDraw.Draw(self.image) # Create a drawing object
            self._render_image_on_canvas() # Render the image on the canvas
    
    # Function to redo the last undone action
    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.image.copy()) # Push the current state to the undo stack
            last_undone = self.redo_stack.pop() # Pop the last undone action from the redo stack
            self.image = last_undone # Set the image to the last undone action
            self.draw = ImageDraw.Draw(self.image) # Create a drawing object
            self._render_image_on_canvas() # Render the image on the canvas

    # Function to render the image on the canvas
    def _render_image_on_canvas(self):
        self.delete("all") # Clear the canvas
        self.tk_img = ImageTk.PhotoImage(self.image) # Create a Tkinter image from the PIL image
        self.create_image(0, 0, anchor="nw", image=self.tk_img) # Create the image on the canvas

    # Function to draw on the canvas
    def paint(self, event):
        # Draw on canvas while moving the mouse if not in fill mode
        if not self.fill_mode:
            self.delete("mouse_cursor") # Remove cursor preview while drawing
            if self.old_x and self.old_y:
                # Eraser mode: Draw line in background color
                if self.eraser_mode:
                    self.create_line(self.old_x, self.old_y, event.x, event.y,
                                        width=self.line_width, fill=self.pen_color,
                                        capstyle=tk.ROUND, smooth=tk.TRUE)
                    self.old_x = event.x
                    self.old_y = event.y

                # Shape mode: Update coordinates of current shape
                elif self.shape in ["Line", "Rectangle", "Circle"]:
                    self.coords(self.temp_shape, self.old_x, self.old_y, event.x, event.y)

                # Freehand mode: Draw line segment
                else:
                    self.create_line(self.old_x, self.old_y, event.x, event.y,
                                            width=self.line_width, fill=self.pen_color,
                                            capstyle=tk.ROUND, smooth=tk.TRUE)
                    self.old_x = event.x
                    self.old_y = event.y

    # Function to reset after mouse release and save current state
    def reset(self, event):
        self.save_state()    
        self.old_x = None
        self.old_y = None

    # Function to set the pen color and disable eraser
    def set_pen_color(self, color):
        self.line_width = self.default_line_width
        self.pen_color = color
        self.eraser_mode = False

    # Function to delete the drawing and reset the canvas, settings
    def delete_drawing(self):
        self.delete("all")
        self.configure(cursor="@assets/pencil.xbm")
        self.pen_color = self.default_pen_color
        self.line_width = self.default_line_width
        with open("state_canvas.ps", "w") as f: # Reset the state file
            pass
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.save_state()
    
    # Function to enable eraser mode
    def set_eraser(self):
        self.eraser_mode = True
        self.pen_color = self['background']
        self.line_width = self.erase_default_line_width
        self.configure(cursor="@assets/eraser.xbm")
        self.fill_mode = False

    # Function to track the mouse cursor (mouse preview)
    def track_mouse(self, event):
        self.delete("mouse_cursor")
        self.create_oval(event.x - self.line_width / 2, event.y - self.line_width / 2,
                        event.x + self.line_width / 2, event.y + self.line_width / 2,
                        fill=self.pen_color, outline="grey", tag="mouse_cursor", width=1)
    
    # Function to set the current shape to draw
    def set_shape(self, shape):
        self.shape = shape
        self.configure(cursor="@assets/pencil.xbm")
        self.eraser_mode = False
        self.fill_mode = False 

    # Function to set the normal drawing mode
    def normal_drawing(self):
        self.eraser_mode = False
        self.pen_color = self.default_pen_color
        self.line_width = self.default_line_width
        self.configure(cursor="@assets/pencil.xbm")
        self.fill_mode = False

    # Function to set the brush size
    def set_brush_size(self, size):
        self.line_width = size

    # Function to enable the fill mode
    def set_fill_mode(self):
        self.eraser_mode = False
        self.fill_mode = True
        self.pen_color = self.default_pen_color
        self.line_width = self.default_line_width
        self.configure(cursor="@assets/fill.xbm")
    
    # Function to fill area of shape at coordinates (x, y)
    def fill_area(self, x, y):
        overlapping = self.find_overlapping(x - 1, y - 1, x + 1, y + 1) # Find overlapping shapes
        if overlapping: # If there are overlapping shapes
            shape_id = overlapping[0] # Get the first overlapping shape
            self.itemconfig(shape_id, fill=self.pen_color) # Fill the shape with the pen color

    # Function to open an image from the file system
    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")]) # Open file dialog
        if file_path: # If a file is selected
            img = Image.open(file_path) # Open the image
            self.image = img.copy() # Copy the image to the canvas image
            self.draw = ImageDraw.Draw(self.image) # Create a drawing object
            self.tk_img = ImageTk.PhotoImage(img) # Create a Tkinter image from the PIL image
            self.create_image(0, 0, anchor="nw", image=self.tk_img) # Create the image on the canvas

    # Function to save the image to the file system
    def save_image(self):
        self.delete("mouse_cursor") # Remove cursor preview before saving
        # Open file dialog to save the image
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]) 
        if file_path: # If a file path is selected
            ps_file = "image_canvas.ps" # Postscript file for saving the image
            self.postscript(file=ps_file, colormode='color') # Save the current state to the postscript file
            img = Image.open(ps_file) # Open the saved postscript file
            img.save(file_path)  # Save to the specified path
            img.close() # Close the image
            # Optionally delete the temp file
            import os
            os.remove(ps_file)