import tkinter as tk
from tkinter import colorchooser

class Toolbar(tk.Frame):
    def __init__(self, master=None, set_color=None, clear_space=None, set_eraser=None):
        super().__init__(master)
        self.master = master
        self.set_color = set_color
        self.clear_space = clear_space
        self.set_eraser = set_eraser
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.color_image = tk.PhotoImage(file="assets/colour.png").subsample(14)
        self.color_button = tk.Button(self, image=self.color_image, command=self.choose_color)
        self.color_button.pack(side="left", padx=5)

        self.color_label = tk.Label(self, bg="black", width=4, height = 2, relief="sunken")
        self.color_label.pack(side="left", padx=5)

        self.clear_button = tk.Button(self, text="Clear", command=self.reset_clear_space)
        self.clear_button.pack(side="left", padx=5)

        self.eraser = tk.PhotoImage(file="assets/eraser.png").subsample(14)
        self.eraser_button = tk.Button(self, image=self.eraser, command=self.set_eraser)
        self.eraser_button.pack(side="left", padx=5)

    def choose_color(self, color = "black"):
        color = colorchooser.askcolor(title="Choose a color")
        if color:
            self.color_label.config(background=str(color[1]))
            self.set_color(color[1])
    
    def reset_clear_space(self):
        self.clear_space()
        self.color_label.config(background="black")