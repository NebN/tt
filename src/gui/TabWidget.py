import os
import sys
from PyQt5.QtWidgets import QTabWidget, QToolButton, QMenu, QWidget, QFileDialog, QTabBar
from src.controller import Controller, UserAction
from .WorkSheet import WorkSheet
from .Dialog import Dialog


class TabWidget(QTabWidget):
    def __init__(self, master=None):
        QTabWidget.__init__(self, master)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self._handle_close_requested)

        # New Tab 'Button'
        self.addTab(QWidget(self), ' + ')
        # remove 'delete tab' button from the ' + ' tab
        self.tabBar().setTabButton(0, QTabBar.RightSide, None)
        self.currentChanged.connect(self._handle_tab_changed)

        # Initial Tab
        tab = WorkSheet()
        Controller(tab)
        self.add(tab, 'new tab')

        # Menu
        self.menu = QToolButton(self)
        self.menu.setText('menu')
        self.menu.setMinimumSize(45, 30)
        self.menu.setPopupMode(QToolButton.InstantPopup)
        m = QMenu()
        for action in UserAction:
            m.addAction(action.label)
        self.menu.setMenu(m)
        self.menu.triggered.connect(self._handle_menu_action)
        self.setCornerWidget(self.menu)

    def _len(self):
        return len(self)

    def _current(self):
        return self.currentWidget()

    def add(self, tab, name):
        index = self._len() - 1
        self.insertTab(index, tab, name)
        self.setCurrentIndex(index)

    # TODO handle file save on close or persistence between sessions
    def _handle_close_requested(self, index):
        if self._len() == 2:
            sys.exit(0)

        if index == self._len() - 2:
            self.setCurrentIndex(index - 1)
        self.removeTab(index)

    def _handle_tab_changed(self, _):
        if self.currentIndex() == self._len() - 1:
            tab = WorkSheet()
            Controller(tab)
            self.add(tab, 'new tab')

    def _handle_menu_action(self, event):
        if event.text() == UserAction.OPEN.label:
            self._open()
        elif event.text() == UserAction.SAVE.label:
            self._save()
        elif event.text() == UserAction.INFO.label:
            self._info()

    def _open(self):
        file, _ = QFileDialog.getOpenFileName(None,
                                              'Select a transformation file',
                                              '', 'TextTransformation (*.tt)')

        if file:
            with open(file) as code:
                filename = os.path.basename(file).split('.')[-2]
                tab = WorkSheet()
                Controller(tab)
                tab.code.set(code.read())
                self.add(tab, filename)

    def _save(self):
        filename, _ = QFileDialog.getSaveFileName(None,
                                                  'Save the current transformation file',
                                                  '', 'TextTransformation (*.tt)')

        if filename:
            with open(filename, 'w+') as file:
                file.write(self._current().code.get())

    def _info(self):
        info = "===== WORK IN PROGRESS =====\n" \
               "\n" \
               "Ctrl + Enter to execute\n" \
               "\n" \
               "commands:\n" \
               "- replace \"regex\" with \"replacement\"\n" \
               "- sort\n" \
               "- sort reverse"
        self._necessaryhandle = Dialog(title='info', message=info)