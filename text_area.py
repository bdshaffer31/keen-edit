''' module containing custom text area class that wraps TK class '''
import tkinter as tk

class TextArea(tk.Text):
    ''' class taht wraps TK text class and gives options like TextModified '''

    def __init__(self, *args, **kwargs):
        ''' text widget that reports on internal widget commands '''
        tk.Text.__init__(self, *args, **kwargs)

        self.yscroll_bar = tk.Scrollbar(self)
        self.xscroll_bar = tk.Scrollbar(self, orient=tk.HORIZONTAL)

        self.yscroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.xscroll_bar.pack(side=tk.BOTTOM, fill=tk.X)
        # Scrollbar will adjust automatically according to the content
        self.yscroll_bar.config(command=self.yview)
        self.xscroll_bar.config(command=self.xview)
        self.config(yscrollcommand=self.yscroll_bar.set)
        self.config(xscrollcommand=self.xscroll_bar.set)

        # wtf does this do
        # add orig to widget name ?
        self._orig = self._w + '_orig'
        self.tk.call('rename', self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        '''  proxy command that generates TextModified event if relevant '''
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ('insert', 'delete', 'replace'):
            self.event_generate('<<TextModified>>')

        return result
