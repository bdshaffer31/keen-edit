''' used by Notepad to open file explorers '''
# maybe should just be a module and not a class
from tkinter import Toplevel, Listbox, END
import os

class FileExplorer:
    ''' class that handles file explorers '''

    def __init__(self, run_path):
        self.run_path = run_path
        self.file_explorer = Listbox()

    def open_file_explorer(self, dir_path):
        ''' opens a new instance of a file explorer in a pop out '''
        # add file explorer
        fe_frame = Toplevel()
        # set dimensions and position
        fe_frame.geometry(f'{300}x{400}+{400}+{400}')
        # add a listbox
        self.file_explorer = Listbox(fe_frame, width=300, height=400)
        self.file_explorer.pack()
        # get file names from current directory (should be the open dir)
        file_names = os.listdir(dir_path)
        for name in file_names:
            self.file_explorer.insert(END, name)

        # bind double click to open new window with that file
        self.file_explorer.bind('<Double-Button-1>', lambda event: self.open_file(dir_path))

    def open_file(self, dir_path):
        ''' called on double click, opens the currently selected file '''
        selection = self.file_explorer.curselection()[0]
        selection_path = os.path.join(dir_path, str(self.file_explorer.get(selection)))
        os.system(f'start {self.run_path} {selection_path}')
