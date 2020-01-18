from tkinter import *
from tkinter.ttk import Notebook
from .Window import Window
from src.controller import Controller


class SuperWindow(Notebook):

    def __init__(self, master):
        Notebook.__init__(self, master=None)
        self.master = master
        self.master.title("TT")
        self.pack(fill=BOTH, expand=1)
        self.bind('<ButtonRelease-1>', self.add_tab)

    def add_window(self, name):
        window = Window(self)
        Controller(window)
        self.add(window, text=name)

    def add_tab(self, _):
        sel = self.select()  # gets id of selected tab

        # if the selected tab is the last tab in the Notebook
        if sel == self.tabs()[-1]:
            # Change the text from '+++' to 'New Tab'
            self.tab(sel, text='New Tab')
            # root.nametowidget is used to map the id to widget
            # this shows adding widgets to the existing tab
            tab_id = self.master.nametowidget(sel)
            window = Window(self)
            Controller(window)
            self.add(window, text='new tab')
            # Label(tab_id, text='This is a new tab').pack()

            # add a new 'New Tab' button
            self.add(Frame(self), text=' + ')

