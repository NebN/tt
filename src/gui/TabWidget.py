import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTabWidget, QToolButton, QMenu, QWidget, QFileDialog, QTabBar, QMessageBox

from src.controller import Controller, UserAction
from .Dialog import Dialog
from .WorkSheet import WorkSheet


class TabWidget(QTabWidget):
    emptied = pyqtSignal(int)

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
        self.add(tab)

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

    def safeclose(self):
        for sheet in self._sheets():
            closed = self._handle_close_requested(self.indexOf(sheet))
            if not closed:
                return False
        return True

    def add(self, tab, name=None):
        if not name:
            new_tab_count = len(list(filter(
                lambda t: t.startswith('new tab'),
                [self.tabText(i) for i in range(0, self._len() - 1)]
            )))
            if new_tab_count == 0:
                name = 'new tab'
            else:
                name = f'new tab ({new_tab_count + 1})'

        index = self._len() - 1
        tab.name.connect(self._handle_name_change)
        self.insertTab(index, tab, name)
        self.setCurrentIndex(index)

    def _sheets(self):
        return [self.widget(n) for n in range(0, self._len() - 1)]

    def _len(self):
        return len(self)

    def _current(self):
        return self.currentWidget()

    def _handle_name_change(self, name):
        # TODO can this be wrong? cab the tab change in the meanwhile?
        self.setTabText(self.currentIndex(), name)

    def _handle_close_requested(self, index):
        tab = self.widget(index)
        if tab.isdirty:
            close = QMessageBox.question(self,
                                         'Warning - file not saved',
                                         f'Save {self.tabText(index)}?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if close == QMessageBox.Yes:
                return self._close_tab(index, save=True)
            elif close == QMessageBox.No:
                return self._close_tab(index, save=False)
            else:
                return False
        else:
            return self._close_tab(index)

    def _close_tab(self, index, save=False):
        close = True

        if save:
            close = self._save(index=index)

        if close:
            if self._len() == 2:
                self.emptied.emit(0)

            if index == self._len() - 2:
                self.setCurrentIndex(index - 1)
            self.removeTab(index)

        return close

    def _handle_tab_changed(self, _):
        if self.currentIndex() == self._len() - 1:
            tab = WorkSheet(self)
            Controller(tab)
            self.add(tab)

    def _handle_menu_action(self, event):
        if event.text() == UserAction.OPEN.label:
            self._open()
        elif event.text() == UserAction.SAVE.label:
            self._save(overwrite=True)
        elif event.text() == UserAction.SAVE_AS.label:
            self._save(overwrite=False)
        elif event.text() == UserAction.INFO.label:
            self._info()

    def _open(self):
        filename, _ = QFileDialog.getOpenFileName(None,
                                                  'Select a transformation file',
                                                  '', 'TextTransformation (*.tt)')

        if filename:
            name = os.path.basename(filename).split('.')[-2]
            tab = WorkSheet.from_file(filename, master=self)
            Controller(tab)
            self.add(tab, name)

    def _save(self, overwrite=True, index=-1):
        tab = self._current() if index == -1 else self.widget(index)
        name = tab.save(overwrite)
        if name:
            tab.setTabText(self.indexOf(tab), name)
        return name is not None

    def _info(self):
        info = "===== WORK IN PROGRESS =====\n" \
               "\n" \
               "shortcuts:\n" \
               "- Ctrl + Enter to execute\n" \
               "- Ctrl + S to save\n" \
               "\n" \
               "commands:\n" \
               "- replace \"regex\" with \"replacement\"\n" \
               "- grep \"regex\"\n" \
               "- distinct\n" \
               "- sort\n" \
               "- sort reverse"
        self._necessaryhandle = Dialog(title='Info', message=info)
