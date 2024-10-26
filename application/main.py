import tkinter as tk
import toolbar as tb
import drawing as dr

class Application(tk.Frame):
    def __init__(self, window_width, window_height, master=None):
        super().__init__(master)
        self.master = master
        tool_bar_height = 70
        drawing_space_height = window_height - tool_bar_height

        tool_bar_frame = tk.Frame(self.master)
        tool_bar_frame.place(x=0, y=0, width=window_width, height=tool_bar_height)

        self.drawing_space = dr.Drawing(self.master, width=window_width, height=drawing_space_height, background='white')
        self.drawing_space.place(x=0, y=tool_bar_height)

        self.toolbar = tb.Toolbar(tool_bar_frame, 
                                  self.drawing_space.set_pen_color, 
                                  self.drawing_space.delete_drawing, 
                                  self.drawing_space.set_eraser,
                                  self.drawing_space.set_shape,
                                  self.drawing_space.normal_drawing,
                                  self.drawing_space.set_brush_size,
                                  self.drawing_space.set_fill_mode,
                                  self.drawing_space.open_image,
                                  self.drawing_space.save_image,
                                  self.drawing_space.undo,
                                  self.drawing_space.redo)
        
        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == '__main__':
    master = tk.Tk()
    master.title('Fake Paint Application')
    window_width = 1000
    window_height = 1000
    master.geometry(str(window_width) + 'x' + str(window_height))
    
    with open("state_canvas.ps", "w") as f:
        pass

    app = Application(window_width, window_height, master=master)
    app.pack()
    app.mainloop()
