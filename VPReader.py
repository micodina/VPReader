#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the VPReader project.
#
# This Source Code Form is subject to the terms of GNU GENERAL PUBLIC LICENSE Version 3, see LICENSE
# Author : Michaël Codina


from VPAgenda import Agenda
from VPConfig import Config
import sys
import os
import webbrowser

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidget, QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QLabel
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt


class ListItems(QListWidget):
    """ ListItems(), an class inherited from QListWidget to list items of an agenda.
    """
    def clicked(self, item):
        # QMessageBox.information(self, "ListWidget", "ListWidget: " + item.text())
        window.indexitem = self.currentRow()
        window.listSlides.update()
        print("{}/{}".format(window.indexitem, window.indexslide))

    def update(self):
        self.clear()
        for item in window.myAgenda.data:
            self.addItem(item.getshort())


class ListSlides(QListWidget):
    """ ListSlides(), an class inherited from QListWidget to list slides of an item.
    """
    def clicked(self, item):
        window.indexslide = self.currentRow()
        print("{}/{}".format(window.indexitem, window.indexslide))

    def update(self):
        self.clear()
        item = window.myAgenda.data[window.indexitem]
        for slide in item.getcontent():
            self.addItem(slide['Text'])


class FullScreenWindow(QWidget):
    """ FullScreenWindow(QWidget) a class inherited for the FullScreen Windows.
    """
    def __init__(self):
        super().__init__()
        # To be modified
        self.setGeometry(0,0,320,240)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("font-size: 48pt;color: white;font-weight: bold;")
        self.footer = QLabel()
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignBottom)
        self.footer.setStyleSheet("font-size: 14pt;color: white;font-weight: bold;")
        fullscreen_layout = QVBoxLayout(self)
        fullscreen_layout.setContentsMargins(0,0,0,0)
        fullscreen_layout.addWidget(self.label)
        fullscreen_layout.addWidget(self.footer)

    def updateLabel(self):
        item = window.myAgenda.data[window.indexitem]
        slide = item.getcontent()[window.indexslide]
        self.footer.show() # Doesn't work...
        if item.gettype()=="Song":
            self.setStyleSheet("background-color: blue;")
            self.label.setText(slide['Text'])
            self.footer.setText(item.getshort())
        elif item.gettype()=="Bible":
            self.setStyleSheet("background-color: grey;")
            self.label.setText(str(slide['ID'])+ " : " + slide['Text'])
            self.footer.setText(item.getshort())
        elif item.gettype()=="Image":
            pixmap = QPixmap(window.myAgenda.dirname+slide['Text'])
            self.label.setPixmap(pixmap.scaled(self.size()))
            self.label.setScaledContents(False)
            self.footer.hide()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape.value:
            self.close()
        elif event.key() == Qt.Key.Key_Up.value:
            window.decrementIndex()
            self.updateLabel()
        elif event.key() == Qt.Key.Key_Down.value:
            window.incrementIndex()
            self.updateLabel()


class MainWindow(QMainWindow):
    """ MainWindow(QWidget) a class inherited for the Main Windows.
    """
    def __init__(self):
        super().__init__()

        self.myConfig = Config()
        self.myAgenda=Agenda()

        # Actions File menu
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+F")
        open_action.triggered.connect(self.doOpenFile)

        close_action = QAction("Close", self)
        close_action.setShortcut("Ctrl+X")
        close_action.triggered.connect(self.doCloseFile)

        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.doQuit)

        # Actions Display menu
        fullscreen_action = QAction("Fullscreen", self)
        fullscreen_action.setShortcut("Ctrl+P")
        fullscreen_action.triggered.connect(self.doFullscreen)

        # Actions Question menu
        help_action = QAction("Help", self)
        help_action.setShortcut("Ctrl+H")
        help_action.triggered.connect(self.doHelp)

        about_action = QAction("About", self)
        about_action.setShortcut("Ctrl+A")
        about_action.triggered.connect(self.doAbout)
                                       
        # Creation File menu
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

        # Creation Display menu
        display_menu = self.menuBar().addMenu("Display")
        display_menu.addAction(fullscreen_action)

        # Creation Question menu
        question_menu = self.menuBar().addMenu("?")
        question_menu.addAction(help_action)
        question_menu.addAction(about_action)

        # Container widget
        widget = QWidget()
        self.setCentralWidget(widget)

        # Creation listItems
        self.listItems = ListItems(self)
        self.listItems.show()
        self.listItems.itemClicked.connect(self.listItems.clicked)

        # Creation listVerse
        self.listSlides = ListSlides(self)
        self.listSlides.show()
        self.listSlides.itemClicked.connect(self.listSlides.clicked)

        # Creation QHBoxLayout, add QListWidget
        hbox = QHBoxLayout()
        hbox.addWidget(self.listItems)
        hbox.addWidget(self.listSlides)
        widget.setLayout(hbox)

        # To be modified
        self.setGeometry(100, 100, 600, 400)

        self.setWindowTitle("VPReader")
        self.fullScreenWindow = FullScreenWindow()

    def incrementIndex(self):
        item = self.myAgenda.data[self.indexitem]
        NItems = self.myAgenda.data.__len__()
        NSlides = item.getcontent().__len__()
        if self.indexslide < NSlides-1:
            self.indexslide = self.indexslide+1
        else:
            if self.indexitem < NItems-1:
                self.indexitem = self.indexitem+1
                self.indexslide = 0

    def decrementIndex(self):
        if self.indexslide > 0:
            self.indexslide = self.indexslide-1
        elif self.indexitem > 0:
            self.indexitem = self.indexitem-1
            item = self.myAgenda.data[self.indexitem]
            NSlides = item.getcontent().__len__()
            self.indexslide = NSlides-1

    def doOpenFile(self):
        fname = QFileDialog.getOpenFileName(
            self,  "Open File", self.myConfig.preferences["directory"], "VideoPsalm Agenda (*.vpagd);;All Files (*)")
        if fname[0]:
            self.OpenFile(fname[0])
            self.myConfig.preferences["directory"] = os.path.dirname(fname[0])
            self.myConfig.save()

    def OpenFile(self, filename):
        self.myAgenda = Agenda(filename)
        self.setWindowTitle("VPReader : " + os.path.basename(self.myAgenda.filename))

        self.indexitem = 0
        self.indexslide = 0
        self.listItems.update()
        self.listSlides.update()
        self.listItems.setCurrentRow(0)
        self.listSlides.setCurrentRow(0)

    def doCloseFile(self):
        if not(len(self.myAgenda.data)==0):
            del self.myAgenda
        self.listSlides.clear()
        self.listItems.clear()
        self.setWindowTitle("VPReader")

    def doQuit(self):
        self.close()
        QApplication.quit()
        return

    def doFullscreen(self):
        if len(screens)>1:
            self.move(app.screens()[1].geometry().topLeft())
        self.fullScreenWindow.showFullScreen()
        self.fullScreenWindow.updateLabel()
    
    def doAbout(self):
        QMessageBox.information(self, "VPReader : About", "VPReader version a0.03, 5/23/2023")

    def doHelp(self):
        url="https://github.com/micodina/VPReader"
        webbrowser.open(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screens=app.screens()
    for sc in screens:
        print(sc.name())
    window = MainWindow()
    window.show()
    if len(sys.argv) > 1:
        window.OpenFile(sys.argv[1])
    sys.exit(app.exec())
