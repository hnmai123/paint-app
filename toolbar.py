import tkinter as tk
from tkinter import colorchooser

class Toolbar(tk.Frame):
    def __init__(self, master=None, set_color=None, clear_space=None):
        super().__init__(master)
        self.master = master
        self.set_color = set_color
        self.clear_space = clear_space
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.color_image = tk.PhotoImage(file="assets/colour.png").subsample(15)
        self.color_button = tk.Button(self, image=self.color_image, command=self.choose_color)
        self.color_button.pack(side="left")

        self.color_label = tk.Label(self, bg="black", width=5, height =5, relief="sunken")
        self.color_label.pack(side="left")

        self.clear_button = tk.Button(self, text="Clear", command=self.clear_space)
        self.clear_button.pack(side="left")
    
    def choose_color(self, color = "black"):
        color = colorchooser.askcolor(title="Choose a color")
        if color:
            self.color_label.config(background=str(color[1]))
            self.set_color(color[1])