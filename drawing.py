import tkinter as tk

class Drawing(tk.Canvas):
    def __init__(self, master=None, width =None, height = None, background = None):
        super().__init__(master, width = width, height = height, background=background)
        self.master = master

        self.old_x = None
        self.old_y = None
        self.pen_color = "black"
        self.line_width = 5

        self.bind('<Button-1>', self.activate_paint)
        self.bind('<B1-Motion>', self.paint)
        self.bind('<ButtonRelease-1>', self.reset)

    def activate_paint(self, event):
        self.old_x = event.x
        self.old_y = event.y
        self.create_oval(event.x - self.line_width / 2, event.y - self.line_width / 2,
                            event.x + self.line_width / 2, event.y + self.line_width / 2,
                            fill=self.pen_color, outline=self.pen_color)
        
    def paint(self, event):
        if self.old_x and self.old_y:
            self.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=self.line_width, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.old_x = event.x
            self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None

    def set_pen_color(self, color):
        self.pen_color = color

    def delete_drawing(self):
        self.delete("all")
