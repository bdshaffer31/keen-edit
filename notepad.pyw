''' main module containing note-ad class'''
import tkinter as tk
import os
import subprocess
import sys
import difflib
# To get the space above for message
from tkinter.messagebox import showinfo
# To get the dialog box to open when required
from tkinter.filedialog import askopenfilename, asksaveasfilename
from ctypes import windll
from pygments import lex
# unused
#from pygments import highlight
from pygments.lexers.python import PythonLexer

from color_set import ColorSet
from file_explorer import FileExplorer
from terminal_interface import TerminalInterface
from text_area import TextArea


class Notepad:
    ''' class that creates notepad and controls  '''
    root = tk.Tk()

    # fixes the resolution
    windll.shcore.SetProcessDpiAwareness(1)

    # default window width and height
    width = 400
    height = 500
    #text_area = tk.Text(root, wrap="none")
    text_area = TextArea(root, wrap="none")
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    view_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu = tk.Menu(menu_bar, tearoff=0)
    font_menu = tk.Menu(menu_bar, tearoff=0)
    run_menu = tk.Menu(menu_bar, tearoff=0)

    popup_menu = tk.Menu(menu_bar, tearoff=0)
    auto_sug_menu = tk.Menu(menu_bar, tearoff=0)

    # To add scrollbar
    file = None

    def __init__(self, **kwargs):
        '''
        initialize notpad object with
            needed menus,
            color theme handler,
            file explorer
        '''
        self.color_set = ColorSet()
        self.color_set.set_kimbie_dark()
        self.unsaved_changes = False
        self.run_path = os.path.abspath('notepad.pyw')
        self.file_explorer = FileExplorer(self.run_path)
        self.font_size = 10
        self.font_style = 'Courier'
        self.line_viewed = 1.0
        self.use_syntax_hl = True

        # Set icon
        try:
            self.root.wm_iconbitmap("Notepad.ico")
        except tk.TclError:
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

        # set up root before checking file loads
        self.root.title("Untitled - Notepad")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close_root)

        # add run menu features then add to menu bar
        self.run_menu.add_command(label='Compile', state='disabled')
        self.run_menu.add_command(label='Pylint', state='disabled')
        self.run_menu.add_command(label='Run', state='disabled')

        # set text area and header to last opened file
        try:
            self.file_path = kwargs['file_path']
            self.set_from_file(self.file_path)
        except KeyError:
            try:
                self.file_path = self.read_last_opened()
                if self.file_path:
                    self.set_from_file(self.file_path)
            except ValueError:
                print('latest_file.txt corrupted')

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
        self.text_area.grid(sticky=tk.N + tk.E + tk.S + tk.W)

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

        # Add copy paste cut into edit menu and add edit menu to bar
        self.edit_menu.add_command(label='Cut', command=self.__cut)
        self.edit_menu.add_command(label='Copy', command=self.__copy)
        self.edit_menu.add_command(label='Paste', command=self.__paste)

        # add view menu features and then add to menu bar
        self.view_menu.add_command(label='Open Console', command=self.open_console)
        self.view_menu.add_command(label='Toggle Syntax Highlight', command=self.toggle_syntax_highlight)
        #self.view_menu.add_checkbutton(label='Toggle Syntax Highlight', onvalue=1, offvalue=0, variable=self.use_syntax_hl)
        self.view_menu.add_command(label='New Window', command=self.open_new_window)
        self.view_menu.add_command(label='File Explorer', command=self.open_file_exp)

        # add font menu features then add to menu bar
        self.font_menu.add_command(label='Size Up', command=lambda: self.set_font(self.font_style, self.font_size+2))
        self.font_menu.add_command(label='Size Down', command=lambda: self.set_font(self.font_style, self.font_size-2))
        self.font_menu.add_separator()
        self.font_menu.add_command(label='Courier', command=lambda: self.set_font('Courier', self.font_size))
        self.font_menu.add_command(label='Helvetica', command=lambda: self.set_font('Helvetica', self.font_size))
        self.font_menu.add_command(label='Times New Roman', command=lambda: self.set_font('Times New Roman', self.font_size))
        self.font_menu.add_command(label='FixedSys', command=lambda: self.set_font('Fixedsys', self.font_size))

        # To create a feature of description of the notepad
        self.help_menu.add_command(label='About Notepad', command=self.__show_about)

        # add cascade menus in desired order
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.menu_bar.add_cascade(label='Edit', menu=self.edit_menu)
        self.menu_bar.add_cascade(label='View', menu=self.view_menu)
        self.menu_bar.add_cascade(label='Font', menu=self.font_menu)
        self.menu_bar.add_cascade(label='Run', menu=self.run_menu)
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

	    # adding menu bar to root
        self.root.config(menu=self.menu_bar)

        

        # Bind right click to contect menu
        self.root.bind("<Button-3>", self.context_popup)

        # Bind ctrl-shift to autosuggest menu
        self.root.bind("<Control-Shift_L>", self.auto_sug_popup)

        # Setup pop up menu
        self.popup_menu.add_command(label='Cut', command=self.__cut)
        self.popup_menu.add_command(label='Copy', command=self.__copy)
        self.popup_menu.add_command(label='Paste', command=self.__paste)
        self.popup_menu.add_command(label='Suggest')

        # Setup auto suggest

        # Save and open on keyboard showrtcuts
        self.text_area.bind('<Control-s>', self.save_file_event)
        self.text_area.bind('<Control-o>', self.open_file_event)

    def quit_application(self):
        '''destroy TK application '''
        self.root.destroy()

    def __show_about(self):
        showinfo('Notepad', 'Benjamin Shaffer')

    def on_close_root(self):
        ''' when X is pressed ... save current open file '''
        latest_file = open('latest_file.txt', 'w')
        if self.file_path:
            latest_file.write(self.file_path)
        else:
            latest_file.write('')
        latest_file.close()
        self.root.destroy()

    def read_last_opened(self):
        ''' read the test file containing the last opened file and return the file path '''
        if os.path.getsize('latest_file.txt') > 0:
            latest_file = open('latest_file.txt', 'r')
            last_line = latest_file.readlines()[-1]
            latest_file.close()
            return last_line
        else:
            return False

    def open_file_exp(self):
        ''' use file explorer class to open a file explorer instance in the current dir '''
        try:
            self.file_explorer.open_file_explorer(self.get_open_dir())
        except TypeError:
            print('no open file')

    def open_new_window(self):
        ''' open a new window of Keen Edit '''
        os.system(f'start {self.run_path}')

    def open_console(self):
        ''' use the terminal interface to open a new terminal '''
        terminal = TerminalInterface()
        terminal.open_terminal()

    def set_font(self, font_style, font_size):
        ''' take in a font _style and font_size and set the font correspondingly '''
        self.font_size = font_size
        self.font_style = font_style
        self.text_area.configure(font=(font_style, font_size))

    def toggle_syntax_highlight(self):
        ''' turn on or off syntax highlighting in current window '''
        self.use_syntax_hl = not self.use_syntax_hl
        self.syntax_highlight(use_lexer=self.use_syntax_hl)

    def config_syntax_theme(self):
        ''' color code text based on tokens taht have been already assigned '''
        for token, color in self.color_set.token_colors.items():
            self.text_area.tag_configure(token, foreground=color)

    def syntax_highlight(self, use_lexer=True):
        ''' use lexer to assign tokens to text '''
        self.line_viewed = self.text_area.index(tk.INSERT)
        data = self.text_area.get('1.0', 'end-1c')
        # set up themes for highlighter
        self.config_syntax_theme()
        self.text_area.delete('1.0', tk.END)
        if use_lexer:
            for token, content in lex(data, PythonLexer()):
                self.text_area.insert(tk.END, content, str(token))
        else:
            for token, content in lex(data, PythonLexer()):
                self.text_area.insert(tk.END, content, 'Token.Name')

        # move the view and cursor
        self.text_area.see(self.line_viewed)
        self.text_area.mark_set(tk.INSERT, self.line_viewed)

    def open_file_event(self, event):
        ''' call open file but handle the event '''
        self.open_file()

    def open_file(self):
        ''' open file box for user to click file to open '''
        file_path = askopenfilename(defaultextension=".txt",
                                    filetypes=[("All Files", "*.*"),
                                               ("Text Documents", "*.txt")])

        if file_path == "":
            # no file to open
            self.file_path = None
        else:
            # Try to open the file
            # set the window title
            self.set_from_file(file_path)

    def set_from_file(self, file_path):
        ''' set the text, menus, and file path from a given file path '''
        file_basename = os.path.basename(file_path)
        self.root.title(os.path.basename(file_basename) + " - Notepad")
        self.text_area.delete(1.0, tk.END)

        in_file = open(file_path, "r")
        self.text_area.insert(1.0, in_file.read())
        in_file.close()

        self.set_run_menus()

        self.file_path = file_path
        self.syntax_highlight(use_lexer=self.use_syntax_hl)

    def set_run_menus(self):
        ''' remove the run menus and reinstantiate to reset the commands '''
        self.run_menu.delete('Compile')
        self.run_menu.delete('Pylint')
        self.run_menu.delete('Run')
        self.run_menu.add_command(label='Compile', command=lambda: self.pylint_errors(self.file_path))
        self.run_menu.add_command(label='Pylint', command=lambda: self.pylint_all(self.file_path))
        self.run_menu.add_command(label='Run', command=lambda: self.run_file(self.file_path))

    # TODO this can't handle nested directories
    # would only return closest dir name
    def get_open_dir(self):
        ''' helper that takes the current file path and gives the current working directory '''
        return os.path.dirname(self.file_path)

    # TODO this should be called on save and highlight errors
    def pylint_errors(self, in_file):
        '''
        called by "compile" menu command,
        runs pylint but checking only for errors
        '''
        cmd = f'python -m pylint --errors-only {in_file}'
        subprocess.call(cmd, shell=True)

    def pylint_all(self, in_file):
        ''' pylint the file and print all linting to terminal '''
        cmd = f'python -m pylint {in_file}'
        subprocess.call(cmd, shell=True)

    def run_file(self, in_file):
        ''' run the current file by calling python FILENAME '''
        cmd = f'python {in_file}'
        subprocess.call(cmd, shell=True, cwd=self.get_open_dir())

    # TODO add are you sure menu
    def new_file(self):
        ''' clear text area and set up untitled file'''
        self.root.title('Untitled - Notepad')
        self.file_path = None
        self.text_area.delete(1.0, tk.END)

    # TODO remove this?
    def read_text_input(self):
        ''' reads text area and prints all contents? '''
        text_read = self.text_area.get('1.0', 'end-1c')
        print(text_read)

    def set_text(self, value):
        ''' clear text area and insert given text '''
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, value)

    def save_file_event(self, event):
        ''' call save file and handle event '''
        self.save_file()

    def save_file(self):
        ''' give user save file menu '''
        if self.file_path is None:
            # Save as new file
            self.file_path = asksaveasfilename(initialfile='Untitled.txt',
                                          defaultextension='.txt',
                                          filetypes=[('All Files', '*.*'),
                                                     ('Text Documents', '*.txt')])
            if self.file_path == '':
                self.file_path = None
            else:
                # Try to save the file
                file = open(self.file_path, 'w')
                file.write(self.text_area.get(1.0, tk.END))
                file.close()

                # Change the window title
                self.root.title(os.path.basename(self.file_path) + ' - Notepad')
        else:
            file = open(self.file_path, 'w')
            file.write(self.text_area.get(1.0, tk.END))
            file.close()
        self.syntax_highlight(use_lexer=self.use_syntax_hl)

    def tab(self, event):
        ''' use custom tab of four spaces '''
        self.text_area.insert(tk.INSERT, ' ' * 4)
        return 'break'

    def __cut(self):
        self.text_area.event_generate('<<Cut>>')

    def __copy(self):
        self.text_area.event_generate('<<Copy>>')

    def __paste(self):
        self.text_area.event_generate('<<Paste>>')

    def context_popup(self, event):
        ''' open the suggestions context menu '''
        try:
            self.popup_menu.delete('Suggest')
            self.popup_menu.add_command(label='Suggest', command=lambda: self.auto_sug_popup(event))
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def get_selected(self, detailed=False):
        '''
        return the selected text,
        if detailed is true return the start and end indices
        '''
        start_index = self.text_area.index("sel.first")
        end_index = self.text_area.index("sel.last")
        selected_text = self.text_area.get(start_index, end_index)
        if detailed is False:
            return selected_text
        elif detailed is True:
            return selected_text, start_index, end_index

    def get_suggestions(self, input_s):
        data = self.text_area.get('1.0', 'end-1c')
        text_list = []
        excluded_tokens = ['Token.Comment', 'Token.Comment.Single']
        for token, content in lex(data, PythonLexer()):
            if token not in excluded_tokens:
                text_list.append(content)
        text_list = list(set(text_list))
        sugs = difflib.get_close_matches(input_s, text_list, n=5, cutoff=0.3)
        return sugs

    def replace_text(self, new_text, range_start, range_end):
        ''' delete the text between the given indices and replace with input text '''
        self.text_area.delete(range_start, range_end)
        self.text_area.insert(range_start, new_text)

    def auto_sug_popup(self, event):
        ''' populate the auto suggestions menu '''
        # reinitialize menu to delete menu options without TCl Error
        if self.auto_sug_menu.index('end') is not None:
            self.auto_sug_menu = tk.Menu(self.menu_bar, tearoff=0)

        try:
            sel, start_i, end_i = self.get_selected(detailed=True)
            suggestions = self.get_suggestions(sel)
            # add menu options for suggestions
            for sug in suggestions:
                self.auto_sug_menu.add_command(label=sug, command=lambda sel=sug: self.replace_text(sel, start_i, end_i))
            self.auto_sug_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.auto_sug_menu.grab_release()

    def run(self):
        ''' run the main loop of the TK application '''
        # Run main application
        self.root.mainloop()


if __name__ == '__main__':
    # get input from system if its there
    try:
        PATH_INPUT = sys.argv[1]
    except IndexError:
        PATH_INPUT = None

    # run main application
    if PATH_INPUT is not None:
        NOTEPAD = Notepad(width=800, height=700, file_path=PATH_INPUT)
        NOTEPAD.run()
    else:
        NOTEPAD = Notepad(width=800, height=700)
        NOTEPAD.run()
 