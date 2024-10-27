import tkinter as tk
import toolbar as tb
import drawing as dr

# Application class inherits from tk.Frame and set up the main window of the application
class Application(tk.Frame):
    def __init__(self, window_width, window_height, master=None):
        super().__init__(master)
        self.master = master

        # Set height of the toolbar and the drawing space
        tool_bar_height = 70
        drawing_space_height = window_height - tool_bar_height

        # Create the toolbar frame
        tool_bar_frame = tk.Frame(self.master)
        tool_bar_frame.place(x=0, y=0, width=window_width, height=tool_bar_height)

        # Create the drawing space
        self.drawing_space = dr.Drawing(self.master, width=window_width, height=drawing_space_height, background='white')
        self.drawing_space.place(x=0, y=tool_bar_height)

        # Initialize the toolbar with callbacks for the drawing actions
        self.toolbar = tb.Toolbar(tool_bar_frame, 
                                  self.drawing_space.set_pen_color, # Change the pen color
                                  self.drawing_space.delete_drawing, # Clear the drawing space
                                  self.drawing_space.set_eraser, # Set the eraser mode
                                  self.drawing_space.set_shape, # Set the shape to draw
                                  self.drawing_space.normal_drawing, # Set the normal drawing mode
                                  self.drawing_space.set_brush_size, # Set the brush size
                                  self.drawing_space.set_fill_mode, # Set the fill mode
                                  self.drawing_space.open_image, # Open image from the file system
                                  self.drawing_space.save_image, # Save image to the file system
                                  self.drawing_space.undo, # Undo the last action
                                  self.drawing_space.redo) # Redo the last undone action
        
        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Main function to run the application
if __name__ == '__main__':
    master = tk.Tk() # Create the main window
    master.title('Fake Paint Application') # Set the title of the window
    window_width = 1000 
    window_height = 1000
    master.geometry(str(window_width) + 'x' + str(window_height)) # Set the size of the window

    # Create or reset the state_canvas.ps file to store the state of the drawing
    with open("state_canvas.ps", "w") as f:
        pass

    # Create the application, initialize and run the main loop
    app = Application(window_width, window_height, master=master)
    app.pack()
    master.mainloop() # Run the tkinter event loop
