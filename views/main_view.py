#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the VPReader project.
#
# This Source Code Form is subject to the terms of GNU GENERAL PUBLIC LICENSE Version 3, see LICENSE
# Author : Michaël Codina


from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QListWidget
from PySide6.QtCore import Slot, QEvent, QObject, Qt
from views.main_view_ui import Ui_MainWindow
from views.VPConfig import Config

import os
import webbrowser


class MainView(QMainWindow):
    """ MainView(), the main view of VPReader used by Model and MainController.
    """

    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._ui.actionFullscreen.setEnabled(False)

        self._my_config = Config()

        # connect widgets to controller
        self._ui.listItems.currentRowChanged.connect(
            self._main_controller.item_changed)
        self._ui.listSlides.currentRowChanged.connect(
            self._main_controller.slide_changed)

        # connect menu actions to controller
        self._ui.actionOpen.triggered.connect(self.do_open_file)
        self._ui.actionClose.triggered.connect(self.do_close_file)
        self._ui.actionQuit.triggered.connect(self.do_quit)
        self._ui.actionFullscreen.triggered.connect(self.do_fullscreen)
        self._ui.actionAbout.triggered.connect(self.do_about)
        self._ui.actionHelp.triggered.connect(self.do_help)

        # listen for model event signals
        self._model.listItems_changed.connect(self.on_listItemschanged)
        self._model.listSlides_changed.connect(self.on_listSlideschanged)
        self._model.details_changed.connect(self.on_detailschanged)
        self._model.preview_changed.connect(self.on_previewchanged)
        self._model.selection_changed.connect(self.on_selectionchanged)

        # Keypress event
        self.keyPressEvent = self.handle_key_press_event

    def setfullscreen_view(self, fullscreenview):
        self._fullscreenview = fullscreenview

    @Slot(list)
    def on_listItemschanged(self, value):
        # print("on_listItemschanged :" + str(value))
        for it in value:
            self._ui.listItems.addItem(it)
        self._ui.listItems.setCurrentRow(0)

    @Slot(list)
    def on_listSlideschanged(self, value):
        # print("on_listSlideschanged :" + str(value))
        self._ui.listSlides.clear()
        for it in value:
            self._ui.listSlides.addItem(it)
        self._ui.listSlides.setCurrentRow(0)

    @Slot(str)
    def on_detailschanged(self, value):
        # print("on_detailschanged :" + str(value))
        self._ui.labelDetails.setText(value)

    @Slot(str)
    def on_previewchanged(self, value):
        # print("on_previewchanged :" + str(value))
        self._ui.labelPreview.setText(value)

    @Slot(int, int)
    def on_selectionchanged(self, item, slide):
        self._ui.listItems.setCurrentRow(item)
        self._ui.listSlides.setCurrentRow(slide)

    def do_open_file(self):
        fname = QFileDialog.getOpenFileName(
            self,  "Open File", self._my_config.preferences["directory"], "VideoPsalm Agenda (*.vpagd);;All Files (*)")
        if fname[0]:
            self._main_controller.do_open_file(fname[0])
            self._my_config.preferences["directory"] = os.path.dirname(
                fname[0])
            self._my_config.save()
            self.setWindowTitle("VPReader - " + os.path.basename(fname[0]))
            self._ui.actionFullscreen.setEnabled(True)

    def do_close_file(self):
        self._main_controller.do_close_file()
        self._ui.listItems.clear()
        self._ui.listSlides.clear()
        self._ui.labelDetails.setText("")
        self._ui.labelPreview.setText("")
        self.setWindowTitle("VPReader")
        self._ui.actionFullscreen.setEnabled(False)

    def do_quit(self):
        self.close()
        self._fullscreenview.close()
        return

    def do_fullscreen(self):
        # self._fullscreenview.showFullScreen()
        self._fullscreenview.show()
        self.activateWindow()

    def do_about(self):
        QMessageBox.information(self, "VPReader : About",
                                "VPReader version a0.04, 6/26/2023")

    def do_help(self):
        url = "https://github.com/micodina/VPReader"
        webbrowser.open(url)

    def handle_key_press_event(self, event):
        if event.key() == Qt.Key_Down:
            self._main_controller.jump("down")
        elif event.key() == Qt.Key_Up:
            self._main_controller.jump("up")
        elif event.key() == Qt.Key.Key_Escape.value:
            self._fullscreenview.close()
        return super().keyPressEvent(event)
