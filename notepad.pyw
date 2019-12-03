import tkinter as tk
import os
import sys
#from tkinter import * #is this even necessary?
# To get the space above for message
from tkinter.messagebox import *
# To get the dialog box to open when required
from tkinter.filedialog import *
import pygments
from pygments import lex
from pygments import highlight
from pygments.lexers.python import PythonLexer

import ctypes
from ctypes import *
from tkinter.tix import *

from color_set import ColorSet
from file_explorer import FileExplorer
from terminal_interface import TerminalInterface


class Notepad:
    root = Tk()

    # fixes the resolution
    windll.shcore.SetProcessDpiAwareness(1)

    # default window width and height
    width = 400
    height = 500
    text_area = Text(root, wrap="none")
    menu_bar = Menu(root)
    file_menu = Menu(menu_bar, tearoff=0)
    edit_menu = Menu(menu_bar, tearoff=0)
    view_menu = Menu(menu_bar, tearoff=0)
    help_menu = Menu(menu_bar, tearoff=0)

    popup_menu = Menu(menu_bar, tearoff=0)

    # To add scrollbar
    yscroll_bar = Scrollbar(text_area)
    xscroll_bar = Scrollbar(text_area, orient=HORIZONTAL)
    file = None

    def __init__(self, **kwargs):
        self.color_set = ColorSet()
        self.color_set.set_kimbie_dark()
        self.unsaved_changes = False
        self.run_path = os.path.abspath('notepad.pyw')
        self.file_explorer = FileExplorer(self.run_path)

        # Set icon
        try:
            self.root.wm_iconbitmap("Notepad.ico")
        except:
            print('icon not found')

        # Set window size (the default is 300x300)
        try:
            self.width = kwargs['width']
        except KeyError:
            pass
        try:
            self.height = kwargs['height']
        except KeyError:
            pass

        # Set the window text
        self.root.title("Untitled - Notepad")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close_root)

        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # For left-allign
        left = (screen_width / 2) - (self.width / 2)

        # For right-allign
        top = (screen_height / 2) - (self.height /2)

        # For top and bottom
        self.root.geometry(f'{self.width}x{self.height}+{int(left)}+{int(top)}')

        # To make the textarea auto resizable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.text_area.grid(sticky=N + E + S + W)

        # text area configurations
        self.text_area.bind('<Tab>', self.tab)
        self.text_area.configure(background=self.color_set.background_color)
        self.text_area.configure(selectbackground=self.color_set.select_color)
        self.text_area.configure(foreground=self.color_set.main_text_color)
        self.text_area.configure(insertbackground=self.color_set.main_text_color)

        # add file menu options and then add to menu bar
        self.file_menu.add_command(label='New', command=self.new_file)
        self.file_menu.add_command(label='Open', command=self.open_file)
        self.file_menu.add_command(label='Save', command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.quit_application)

        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        # Add copy paste cut into edit menu and add edit menu to bar
        self.edit_menu.add_command(label='Cut', command=self.__cut)
        self.edit_menu.add_command(label='Copy', command=self.__copy)
        self.edit_menu.add_command(label='Paste', command=self.__paste)

        self.menu_bar.add_cascade(label='Edit', menu=self.edit_menu)

        # add view menu features and then add to menu bar
        self.view_menu.add_command(label='Open Console', command=self.open_console)
        self.view_menu.add_command(label='Syntax Highlight', command=self.syntax_highlight)
        self.view_menu.add_command(label='New Window', command=self.open_new_window)
        self.view_menu.add_command(label='File Explorer', command=self.open_file_exp)
        self.menu_bar.add_cascade(label='View', menu=self.view_menu)

        # To create a feature of description of the notepad
        self.help_menu.add_command(label='About Notepad', command=self.__show_about)
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

	    # adding menu bar to root
        self.root.config(menu=self.menu_bar)

        self.yscroll_bar.pack(side=RIGHT, fill=Y)
        self.xscroll_bar.pack(side=BOTTOM, fill=X)
        # Scrollbar will adjust automatically according to the content
        self.yscroll_bar.config(command=self.text_area.yview)
        self.xscroll_bar.config(command=self.text_area.xview)
        self.text_area.config(yscrollcommand=self.yscroll_bar.set)
        self.text_area.config(xscrollcommand=self.xscroll_bar.set)

        # Bind right click to contect menu
        self.root.bind("<Button-3>", self.popup)

        # Setup pop up menu
        self.popup_menu.add_command(label='Cut', command=self.__cut)
        self.popup_menu.add_command(label='Copy', command=self.__copy)
        self.popup_menu.add_command(label='Paste', command=self.__paste)

        # Save and open on keyboard showrtcuts
        self.text_area.bind('<Control-s>', self.save_file_event)
        self.text_area.bind('<Control-o>', self.open_file_event)

        # set text area and header to last opened file
        try:
            file_name = kwargs['file_path']
            self.set_from_file(file_name)
        except KeyError:
            file_name = self.read_last_opened()
            if file_name:
                self.set_from_file(file_name)


    def quit_application(self):
        self.root.destroy()
        # exit()

    def __show_about(self):
        showinfo('Notepad', 'Benjamin Shaffer')

    def on_close_root(self):
        latest_file = open('latest_file.txt', 'w')
        if self.file:
            current_path = os.path.abspath(self.file)
            latest_file.write(current_path)
        else:
            latest_file.write('')
        latest_file.close()
        self.root.destroy()

    def read_last_opened(self):
        if os.path.getsize('latest_file.txt') > 0:
            latest_file = open('latest_file.txt', 'r')
            last_line = latest_file.readlines()[-1]
            latest_file.close()
            return last_line
        else:
            return False

    def open_file_exp(self):
        try:
            self.file_explorer.open_file_explorer(self.get_open_dir())
        except TypeError:
            print('no open file')


    def open_new_window(self):
        os.system(f'start {self.run_path}')

    def open_console(self):
        terminal = TerminalInterface()
        terminal.open_terminal()

    def config_syntax_theme(self):
        for token, color in self.color_set.token_colors.items():
            self.text_area.tag_configure(token, foreground=color)

    def syntax_highlight(self):
        data = self.text_area.get("1.0", 'end-1c')

        # set up themes for highlighter
        self.config_syntax_theme()

        self.text_area.delete('1.0', END)
        for token, content in lex(data, PythonLexer()):
            #print(content)
            #print(token)
            #self.text_area.mark_set("range_end", "range_start + %dc" % len(content))
            self.text_area.insert(END, content, str(token))
            #self.text_area.mark_set("range_start", "range_end")

    def open_file_event(self, event):
        self.open_file()

    def open_file(self):
        file_path = askopenfilename(defaultextension=".txt",
                                    filetypes=[("All Files", "*.*"),
                                               ("Text Documents", "*.txt")])

        if file_path == "":
            # no file to open
            self.file = None
        else:
            # Try to open the file
            # set the window title
            self.set_from_file(file_path)

    def set_from_file(self, file_name):
        self.root.title(os.path.basename(file_name) + " - Notepad")
        self.text_area.delete(1.0, END)

        in_file = open(file_name, "r")
        self.text_area.insert(1.0, in_file.read())
        in_file.close()

        self.file = file_name

        self.syntax_highlight()

    def get_open_dir(self):
        return os.path.dirname(self.file)
  
    def new_file(self):
        self.root.title('Untitled - Notepad')
        self.file = None
        self.text_area.delete(1.0,END)

    def read_text_input(self):
        text_read = self.text_area.get('1.0', 'end-1c')
        print(text_read)

    def set_text(self, value):
        self.text_area.delete(1.0, END)
        self.text_area.insert(END, value)

    def save_file_event(self, event):
        self.save_file()

    def save_file(self):
        if self.file is None:
            # Save as new file
            self.file = asksaveasfilename(initialfile='Untitled.txt',
                                          defaultextension='.txt',
                                          filetypes=[('All Files', '*.*'),
                                                     ('Text Documents', '*.txt')])
            if self.file == '':
                self.file = None
            else:
                # Try to save the file
                file = open(self.file, 'w')
                file.write(self.text_area.get(1.0, END))
                file.close()

                # Change the window title
                self.root.title(os.path.basename(self.file) + ' - Notepad')
        else:
            file = open(self.file, 'w')
            file.write(self.text_area.get(1.0, END))
            file.close()
        self.syntax_highlight()

    def tab(self, arg):
        self.text_area.insert(INSERT, ' ' * 4)
        return 'break'

    def __cut(self):
        self.text_area.event_generate('<<Cut>>')
  
    def __copy(self):
        self.text_area.event_generate('<<Copy>>')

    def __paste(self):
        self.text_area.event_generate('<<Paste>>')

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def run(self):
        # Run main application
        self.root.mainloop()


# Run main application
try:
    path_input = sys.argv[1]
    notepad = Notepad(width=800, height=700, file_path=path_input)
    notepad.run()
except IndexError:
    print('no input file')
    notepad = Notepad(width=800, height=700)
    notepad.run()

