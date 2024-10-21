import tkinter as tk
from tkinter import colorchooser

class Toolbar(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.color_button = tk.Button(self, text="Select Color", command=self.choose_color)
        self.color_button.pack(side="left")

        self.color_label = tk.Label(self, bg="white", width=20, relief="sunken")
        self.color_label.pack(side="left")

        self.clear_button = tk.Button(self, text="Clear", command=self.clear_color)
        self.clear_button.pack(side="left")
    
    def choose_color(self):
        color = colorchooser.askcolor(title="Choose a color")
        if color:
            self.color_label.config(background=str(color[1]))
    
    def clear_color(self):
        self.color_label.config(background="white")