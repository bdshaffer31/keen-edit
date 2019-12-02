from tkinter import Toplevel, Listbox, END
import os

class FileExplorer:

    def __init__(self, run_path, directory):
        self.file_explorer = Listbox()
        self.run_path = run_path
        self.current_dir_path = directory

    def set_file_path(self, path):
        self.current_file_path = path

    def open_file_explorer(self):
        # add file explorer
        fe_frame = Toplevel()
        # set dimensions and position
        fe_frame.geometry(f'{300}x{400}+{400}+{400}')
        # add a listbox
        self.file_explorer = Listbox(fe_frame, width = 300, height = 400)
        self.file_explorer.pack()
        # get file names from current directory (should be the open dir)
        file_names = os.listdir(os.path.dirname(self.current_file_path))
        for name in file_names:
            self.file_explorer.insert(END, name)

        # bind double click to open new window with that file
        self.file_explorer.bind('<Double-Button-1>', self.open_file)

    def open_file(self, event):
        selection = self.file_explorer.curselection()[0]
        selection_path = os.path.join(self.current_dir_path, str(self.file_explorer.get(selection)))
        os.system(f'start {self.run_path} {selection_path}')

