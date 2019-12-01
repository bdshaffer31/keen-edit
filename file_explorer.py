from tkinter import Toplevel, Listbox, END
import os

class FileExplorer:

    def __init__(self):
        pass

    def open_file_explorer(self):
        # add file explorer
        fe_frame = Toplevel()
        file_explorer = Listbox(fe_frame)
        file_explorer.pack()
        file_names = os.listdir()
        for name in file_names:
            file_explorer.insert(END, name)