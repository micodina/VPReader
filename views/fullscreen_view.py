#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the VPReader project.
#
# This Source Code Form is subject to the terms of GNU GENERAL PUBLIC LICENSE Version 3, see LICENSE
# Author : Michaël Codina


from PySide6.QtCore import Qt, Slot, QPoint
from PySide6.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument

class FullScreenView(QWidget):
    """ FullScreenView(), the FullScreen view of VPReader used by Model and MainController.
    """

    def __init__(self, model, controller):
        super().__init__()

        self._model = model
        self._fullscreen_controller = controller
        self.setGeometry(0, 0, 800, 600)
        self.label = QLabel(self)
        # self.label.setFrameShape(QFrame.Shape.Box)
        self.label.setWordWrap(True)
        self.label.setStyleSheet(
            "font-size: 48pt;color: white;font-weight: bold;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.footer = QLabel(self)
        # self.footer.setFrameShape(QFrame.Shape.Box)
        self.footer.setStyleSheet(
            "font-size: 14pt;color: white;font-weight: bold;")
        self.footer.setFixedHeight(28)
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pdfview=QPdfView(self)
        self._document=QPdfDocument(self) 
        self.pdfview.setDocument(self._document)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.footer)
        layout.addWidget(self.pdfview)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setFocusPolicy(Qt.NoFocus)

        # listen for model event signals
        self._model.fslabel_song_changed.connect(self.on_fslabel_song_changed)
        self._model.fslabel_bible_changed.connect(self.on_fslabel_bible_changed)
        self._model.fslabel_image_changed.connect(self.on_fslabel_image_changed)
        self._model.fsfooter_changed.connect(self.on_footer_changed)
        self._model.fslabel_black_changed.connect(self.on_fslabel_black_changed)
        self._model.fspdfview_changed.connect(self.on_fspdfview_changed)

    @Slot(str)
    def on_fslabel_bible_changed(self, value):
        # print("on_fslabel_changed")
        self.footer.show()
        self.label.show()
        self.pdfview.hide()
        self.setStyleSheet("background-color: grey;")
        self.label.setText(value)

    @Slot(str)
    def on_fslabel_song_changed(self, value):
        # print("on_fslabel_song_changed")
        self.footer.show()
        self.label.show()
        self.pdfview.hide()
        self.setStyleSheet("background-color: blue;")
        self.label.setText(value)

    @Slot(str)
    def on_fslabel_image_changed(self, value):
        # print("on_fslabel_image_changed" + value)
        self.footer.hide()
        self.pdfview.hide()
        pixmap = QPixmap(value)
        self.label.setPixmap(pixmap.scaled(self.label.size()))
    
    @Slot(str, int)
    def on_fspdfview_changed(self, pdffile, value):
        #print("on_fspdfview_changed {} {}".format(pdffile,value))
        self.footer.hide()
        self.label.hide()
        self.pdfview.show()
        # load the pdf file if needed
        if self._document.pageCount()==0:
            self._document.load(pdffile)
        self.pdfview.setZoomMode(QPdfView.ZoomMode.FitInView)
        if value >=0:
            nav=self.pdfview.pageNavigator()
            nav.jump(value, QPoint(), nav.currentZoom())


    @Slot()
    def on_fslabel_black_changed(self):
        # print("on_fslabel_black_changed")
        self.footer.hide()
        self.label.hide()
        self.pdfview.hide()
        self.setStyleSheet("background-color: black;")

    @Slot(str)
    def on_footer_changed(self, value):
        # print("on_footer_changed")
        self.footer.setText(value)
