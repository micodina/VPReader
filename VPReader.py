#!/usr/bin/env python
# -*- coding: utf-8 -*-
from VPAgenda import Agenda
from VPConfig import Config
import sys
import os
import webbrowser

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidget, QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QLabel
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt


class ListSongs(QListWidget):
    def clicked(self, item):
        # QMessageBox.information(self, "ListWidget", "ListWidget: " + item.text())
        window.indexsong = self.currentRow()
        window.listVerses.update()
        print("{}/{}".format(window.indexsong, window.indexverse))

    def update(self):
        self.clear()
        for song in window.myAgenda.songs:
            self.addItem(str(song['ID'])+":"+song['Text'])


class ListVerses(QListWidget):
    def clicked(self, item):
        window.indexverse = self.currentRow()
        print("{}/{}".format(window.indexsong, window.indexverse))

    def update(self):
        self.clear()
        song = window.myAgenda.songs[window.indexsong]
        for verse in song['Verses']:
            self.addItem(verse['Text'])


class FullScreenWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(
            "font-size: 48pt;color: white;font-weight: bold;")
        self.setStyleSheet("background-color: blue;")
        fullscreen_layout = QVBoxLayout(self)
        fullscreen_layout.addWidget(self.label)

    def updateLabel(self):
        song = window.myAgenda.songs[window.indexsong]
        verse = song['Verses'][window.indexverse]
        self.label.setText(verse['Text'])

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
    def __init__(self):
        super().__init__()

        self.myConfig = Config()

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

        # Creation listSongs
        self.listSongs = ListSongs(self)
        self.listSongs.show()
        self.listSongs.itemClicked.connect(self.listSongs.clicked)

        # Creation listVerse
        self.listVerses = ListVerses(self)
        self.listVerses.show()
        self.listVerses.itemClicked.connect(self.listVerses.clicked)

        # Création QHBoxLayout, add QListWidget
        hbox = QHBoxLayout()
        hbox.addWidget(self.listSongs)
        hbox.addWidget(self.listVerses)
        widget.setLayout(hbox)

        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("VPReader")
        self.fullScreenWindow = FullScreenWindow()

    def incrementIndex(self):
        song = self.myAgenda.songs[self.indexsong]
        NSongs = self.myAgenda.songs.__len__()
        NVerses = song['Verses'].__len__()
        if self.indexverse < NVerses-1:
            self.indexverse = self.indexverse+1
        else:
            if self.indexsong < NSongs-1:
                self.indexsong = self.indexsong+1
                self.indexverse = 0

    def decrementIndex(self):
        if self.indexverse > 0:
            self.indexverse = self.indexverse-1
        elif self.indexsong > 0:
            self.indexsong = self.indexsong-1
            song = self.myAgenda.songs[self.indexsong]
            NVerses = song['Verses'].__len__()
            self.indexverse = NVerses-1

    def doOpenFile(self):
        fname = QFileDialog.getOpenFileName(
            self,  "Open File", self.myConfig.preferences["directory"], "VideoPsalm Agenda (*.vpagd);;All Files (*)")
        if fname[0]:
            self.OpenFile(fname[0])
            self.myConfig.preferences["directory"] = os.path.dirname(fname[0])
            self.myConfig.save()

    def OpenFile(self, filename):
        self.myAgenda = Agenda(filename)
        self.setWindowTitle(
            "VPReader : " + os.path.basename(self.myAgenda.filename))

        self.indexsong = 0
        self.indexverse = 0
        self.listSongs.update()
        self.listVerses.update()
        self.listSongs.setCurrentRow(0)
        self.listVerses.setCurrentRow(0)

    def doCloseFile(self):
        del self.myAgenda
        self.listVerses.clear()
        self.listSongs.clear()
        self.setWindowTitle("VPReader")

    def doQuit(self):
        self.close()
        QApplication.quit()
        return

    def doFullscreen(self):
        self.fullScreenWindow.showFullScreen()
        self.fullScreenWindow.updateLabel()
    
    def doAbout(self):
        QMessageBox.information(self, "VPReader : About", "VPReader version a01, 5/10/2023")

    def doHelp(self):
        url="https://github.com/micodina/VPReader"
        webbrowser.open(url)


#    def keyPressEvent(self, event):
#        if event.key() == Qt.Key.Key_Escape.value:
#            self.fullscreen_window.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    if len(sys.argv) > 1:
        window.OpenFile(sys.argv[1])
    sys.exit(app.exec())
