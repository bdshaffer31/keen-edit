''' module containing TerminalInterface class '''
import os

class TerminalInterface:
    ''' class used to create console instances '''

    def __init__(self):
        self.cmder_path = 'C:\\Users\\Benjamin\\Documents\\cmder_mini\\Cmder.exe'

    def open_terminal(self):
        ''' start the windows command prompt '''
        os.system('start cmd')

    def open_console_emulator(self):
        ''' open a cmder console emulator '''
        os.system(f'start {self.cmder_path}')

    def close_console(self): # not working atm
        ''' close the open terminal, not working '''
        os.system('exit')
