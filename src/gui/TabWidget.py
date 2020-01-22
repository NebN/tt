import os
import sys
from PyQt5.QtWidgets import QTabWidget, QToolButton, QMenu, QWidget, QFileDialog, QTabBar
from src.controller import Controller, UserAction
from .WorkSheet import WorkSheet
from .Dialog import Dialog
from .BinaryDialog import BinaryDialog


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
        tab.name.connect(self._handle_name_change)
        self.insertTab(index, tab, name)
        self.setCurrentIndex(index)

    def _handle_name_change(self, name):
        # TODO can this be wrong? cab the tab change in the meanwhile?
        self.setTabText(self.currentIndex(), name)

    def _handle_close_requested(self, index):
        tab = self.widget(index)
        if tab.isdirty:
            self.dialog = BinaryDialog(self, title=f'Warning - file not saved', message=f'Save {self.tabText(index)}?')
            self.dialog.yes.clicked.connect(lambda: self._close_tab(index, save=True))
            self.dialog.no.clicked.connect(lambda: self._close_tab(index, save=False))
        else:
            self._close_tab(index)

    def _close_tab(self, index, save=False):
        if save:
            self._save(index)

        if self._len() == 2:
            sys.exit(0)

        if index == self._len() - 2:
            self.setCurrentIndex(index - 1)
        self.removeTab(index)

    def _handle_tab_changed(self, _):
        if self.currentIndex() == self._len() - 1:
            tab = WorkSheet(self)
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
        filename, _ = QFileDialog.getOpenFileName(None,
                                                  'Select a transformation file',
                                                  '', 'TextTransformation (*.tt)')

        if filename:
            name = os.path.basename(filename).split('.')[-2]
            tab = WorkSheet.from_file(filename, master=self)
            print(tab.isdirty)
            Controller(tab)
            self.add(tab, name)

    def _save(self, index=-1):
        tab = self._current() if index == -1 else self.widget(index)
        name = tab.save()
        if name:
            tab.setTabText(self.indexOf(tab), name)

    def _info(self):
        info = "===== WORK IN PROGRESS =====\n" \
               "\n" \
               "shortcuts:\n" \
               "- Ctrl + Enter to execute\n" \
               "- Ctrl + S to save\n" \
               "\n" \
               "commands:\n" \
               "- replace \"regex\" with \"replacement\"\n" \
               "- sort\n" \
               "- sort reverse"
        self._necessaryhandle = Dialog(title='Info', message=info)
