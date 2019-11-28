from tkinter import *
import os
import subprocess

class TerminalInterface:

    def __init__(self):
        self.cmder_path = 'C:\\Users\\Benjamin\\Documents\\cmder_mini\\Cmder.exe'
        # root = Tk()
        # termf = Frame(root, height=400, width=500)
        # termf.pack(fill=BOTH, expand=YES)
        # wid = termf.winfo_id()
        #subprocess.call(['C:\\Users\\Benjamin\\Documents\\cmder_mini.exe'])
        #self.console = os.startfile(self.cmder_path )
        #os.system('C:\\Users\\Benjamin\\Documents\\cmder_mini') # %d -geometry 40x20 -sb &' % wid
        #root.mainloop()

    def open_terminal(self):
        os.system('start cmd')

    def open_console_emulator(self):
        os.system(f'start {self.cmder_path}')

    def close_console(self): # not working atm
        os.system('exit')

#import readline # optional, will allow Up/Down/History in the console
# import code
# variables = globals().copy()
# variables.update(locals())
# shell = code.InteractiveConsole(variables)
# shell.interact()