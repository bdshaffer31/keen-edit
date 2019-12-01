import tkinter
import os
from tkinter import * #is this even necessary?
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
import tkinter.font as tkfont

from color_set import ColorSet
from terminal_interface import TerminalInterface


class Notepad:
    
    root = Tk() 

    # fixes the resolution
    windll.shcore.SetProcessDpiAwareness(1)
  
    # default window width and height 
    width = 400
    height = 500
    text_area = Text(root) 
    menu_bar = Menu(root) 
    file_menu = Menu(menu_bar, tearoff = 0) 
    edit_menu = Menu(menu_bar, tearoff = 0)
    view_menu = Menu(menu_bar, tearoff = 0)
    help_menu = Menu(menu_bar, tearoff = 0) 

    popup_menu = Menu(menu_bar, tearoff=0)
      
    # To add scrollbar 
    scroll_bar = Scrollbar(text_area)      
    __file = None
  
    def __init__(self,**kwargs): 

        self.color_set = ColorSet()
        self.unsaved_changes = False

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
        screenWidth = self.root.winfo_screenwidth() 
        screenHeight = self.root.winfo_screenheight() 

        # For left-allign
        left = (screenWidth / 2) - (self.width / 2)  

        # For right-allign 
        top = (screenHeight / 2) - (self.height /2)  

        # For top and bottom 
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, left, top)) 

        # To make the textarea auto resizable 
        self.root.grid_rowconfigure(0, weight=1) 
        self.root.grid_columnconfigure(0, weight=1) 

        # Add controls (widget) 
        self.text_area.grid(sticky = N + E + S + W) 

        # set tab to four spaces
        self.text_area.bind("<Tab>", self.tab)
        self.text_area.configure(background = self.color_set.background_color)

        # add file menu options and then add to menu bar 
        self.file_menu.add_command(label="New", command=self.new_file)   
        self.file_menu.add_command(label="Open", command=self.open_file) 
        self.file_menu.add_command(label="Save", command=self.save_file)            
        self.file_menu.add_separator()                                          
        self.file_menu.add_command(label="Exit", command=self.quit_application) 

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)  

        # Add copy paste cut into edit menu and add edit menu to bar
        self.edit_menu.add_command(label="Cut", command=self.__cut)    
        self.edit_menu.add_command(label="Copy", command=self.__copy)
        self.edit_menu.add_command(label="Paste", command=self.__paste)
        self.edit_menu.add_command(label="Read", command=self.read_text_input)

        self.menu_bar.add_cascade(label="Edit", menu = self.edit_menu)

        # add view menu features and then add to menu bar
        self.view_menu.add_command(label = "Open Console", command = self.open_console)
        self.view_menu.add_command(label = "Syntax Highlight", command = self.syntax_highlight)
        self.menu_bar.add_cascade(label = "View", menu = self.view_menu)

        # To create a feature of description of the notepad 
        self.help_menu.add_command(label="About Notepad", command=self.__showAbout)  
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu) 

	    # adding menu bar to root and filling in right side?
        self.root.config(menu=self.menu_bar) 
        self.scroll_bar.pack(side=RIGHT,fill=Y)

        # Scrollbar will adjust automatically according to the content         
        self.scroll_bar.config(command=self.text_area.yview)      
        self.text_area.config(yscrollcommand=self.scroll_bar.set)    

        # Bind right click to contect menu
        self.root.bind("<Button-3>", self.popup)

        # Setup pop up menu
        self.popup_menu.add_command(label="Cut", command=self.__cut)
        self.popup_menu.add_command(label="Copy", command=self.__copy)
        self.popup_menu.add_command(label="Paste", command=self.__paste)

        # Save and open on keyboard showrtcuts
        self.text_area.bind("<Control-s>", self.save_file_event)
        self.text_area.bind("<Control-o>", self.open_file_event)    

        # set text area and header to last opened file
        file_name = self.read_last_opened()
        if file_name:
            self.set_from_file(file_name)    

    def quit_application(self): 
        self.root.destroy() 
        # exit() 
  
    def __showAbout(self): 
        showinfo("Notepad","Benjamin Shaffer") 

    def on_close_root(self):
        print('on_close called')
        latest_file = open('latest_file.txt', 'w')
        if self.__file:
            current_path = os.path.abspath(self.__file)
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


    def open_console(self):
        terminal = TerminalInterface()
        terminal.open_terminal()

    def config_syntax_theme(self):
        for token, color in self.color_set.token_colors.items():
            self.text_area.tag_configure(token, foreground = color)

    def syntax_highlight(self):
        data = self.text_area.get("1.0",'end-1c')

        # set up themes for highlighter
        self.config_syntax_theme()

        self.text_area.delete('1.0', END)
        for token, content in lex(data, PythonLexer()):
            
            #self.text_area.mark_set("range_end", "range_start + %dc" % len(content))
            self.text_area.insert(END, content, str(token))
            #self.text_area.mark_set("range_start", "range_end")

    def open_file_event(self, event):
        self.open_file()
  
    def open_file(self):
        self.__file = askopenfilename(defaultextension=".txt", 
                                        filetypes=[("All Files","*.*"), 
                                        ("Text Documents","*.txt")]) 
  
        if self.__file == "": 
            # no file to open 
            self.__file = None
        else: 
            # Try to open the file 
            # set the window title 
            self.set_from_file(self.__file)
        
    def set_from_file(self, file_name):
        self.root.title(os.path.basename(file_name) + " - Notepad") 
        self.text_area.delete(1.0,END) 

        in_file = open(file_name,"r") 

        self.text_area.insert(1.0,in_file.read()) 

        in_file.close() 
  
    def new_file(self): 
        self.root.title("Untitled - Notepad") 
        self.__file = None
        self.text_area.delete(1.0,END) 

    def read_text_input(self):
        text_read = self.text_area.get("1.0",'end-1c')
        print(text_read)

    def set_text(self, value):
        self.text_area.delete(1.0, END)
        self.text_area.insert(END, value)

    def save_file_event(self, event):
        self.save_file()
  
    def save_file(self): 
        if self.__file == None: 
            # Save as new file 
            self.__file = asksaveasfilename(initialfile='Untitled.txt', 
                                            defaultextension=".txt", 
                                            filetypes=[("All Files","*.*"), 
                                                ("Text Documents","*.txt")]) 
            if self.__file == "": 
                self.__file = None
            else:   
                # Try to save the file 
                file = open(self.__file,"w") 
                file.write(self.text_area.get(1.0,END)) 
                file.close() 
                  
                # Change the window title 
                self.root.title(os.path.basename(self.__file) + " - Notepad")    
        else: 
            file = open(self.__file,"w") 
            file.write(self.text_area.get(1.0,END)) 
            file.close() 

    def tab(self, arg):
        self.text_area.insert(INSERT, " " * 4)
        return 'break'
  
    def __cut(self): 
        self.text_area.event_generate("<<Cut>>") 
  
    def __copy(self): 
        self.text_area.event_generate("<<Copy>>") 
  
    def __paste(self): 
        self.text_area.event_generate("<<Paste>>") 

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()
        
    def run(self): 
        # Run main application 
        self.root.mainloop() 

  
# Run main application 
notepad = Notepad(width=500,height=600) 
notepad.run() 

