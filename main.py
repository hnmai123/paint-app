import tkinter as tk
import toolbar as tb

class Application(tk.Frame):
    def __init__(self, window_width, window_height, master=None):
        super().__init__(master)
        self.master = master
        tool_bar_height = window_height * 0.2

        tool_bar_frame = tk.Frame(self.master)
        tool_bar_frame.place(x=0, y=0, width=window_width, height=tool_bar_height)

        self.toolbar = tb.Toolbar(tool_bar_frame)
        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


if __name__ == '__main__':
    master = tk.Tk()
    master.title('Fake Paint Application')
    window_width = 1000
    window_height = 1000
    master.geometry(str(window_width) + 'x' + str(window_height))

    app = Application(window_width, window_height, master=master)
    app.pack()
    app.mainloop()
