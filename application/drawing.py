import tkinter as tk

class Drawing(tk.Canvas):
    def __init__(self, master=None, width =None, height = None, background = None):
        super().__init__(master, width = width, height = height, background=background)
        self.master = master
        self.configure(cursor="@assets/pencil.cur")
        self.old_x = None
        self.old_y = None
        self.default_pen_color = "black"    
        self.pen_color = self.default_pen_color
        self.default_line_width = 5
        self.erase_default_line_width = 50
        self.line_width = self.default_line_width
        self.shape = None
        self.eraser_mode = False

        self.bind('<Button-1>', self.activate_paint)
        self.bind('<B1-Motion>', self.paint)
        self.bind('<ButtonRelease-1>', self.reset)
        self.bind('<Motion>', self.track_mouse)

    def activate_paint(self, event):
        self.old_x = event.x
        self.old_y = event.y
    
        if self.shape == "Line":
            self.temp_shape = self.create_line(self.old_x, self.old_y, event.x, event.y, fill=self.pen_color, width=self.line_width)
        elif self.shape == "Rectangle":
            self.temp_shape = self.create_rectangle(self.old_x, self.old_y, event.x, event.y, outline=self.pen_color, width=self.line_width)
        elif self.shape == "Circle":
            self.temp_shape = self.create_oval(self.old_x, self.old_y, event.x, event.y, outline=self.pen_color, width=self.line_width)
        elif not self.eraser_mode:
            self.create_oval(event.x - self.line_width / 2, event.y - self.line_width / 2,
                            event.x + self.line_width / 2, event.y + self.line_width / 2,
                            fill=self.pen_color, outline=self.pen_color)
    
    def paint(self, event):
        self.delete("mouse_cursor")
        if self.old_x and self.old_y:
            if self.eraser_mode:
                self.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=self.line_width, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
                self.old_x = event.x
                self.old_y = event.y

            elif self.shape in ["Line", "Rectangle", "Circle"]:
                self.coords(self.temp_shape, self.old_x, self.old_y, event.x, event.y)
                
            else:
                self.create_line(self.old_x, self.old_y, event.x, event.y,
                                        width=self.line_width, fill=self.pen_color,
                                        capstyle=tk.ROUND, smooth=tk.TRUE)
                self.old_x = event.x
                self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None

    def set_pen_color(self, color):
        self.configure(cursor="@assets/pencil.cur")
        self.line_width = self.default_line_width
        self.pen_color = color
        self.eraser_mode = False

    def delete_drawing(self):
        self.delete("all")
        self.configure(cursor="@assets/pencil.cur")
        self.pen_color = self.default_pen_color
        self.line_width = self.default_line_width
    
    def set_eraser(self):
        self.eraser_mode = True
        self.pen_color = self['background']
        self.line_width = self.erase_default_line_width
        self.configure(cursor="@assets/eraser.cur")

    def track_mouse(self, event):
        self.delete("mouse_cursor")
        self.create_oval(event.x - self.line_width / 2, event.y - self.line_width / 2,
                        event.x + self.line_width / 2, event.y + self.line_width / 2,
                        fill=self.pen_color, outline="grey", tag="mouse_cursor", width=1)
    
    def set_shape(self, shape):
        self.shape = shape
        self.configure(cursor="@assets/pencil.cur")

    def normal_drawing(self):
        self.eraser_mode = False
        self.pen_color = self.default_pen_color
        self.line_width = self.default_line_width
        self.configure(cursor="@assets/pencil.cur")

    def set_brush_size(self, size):
        self.line_width = size