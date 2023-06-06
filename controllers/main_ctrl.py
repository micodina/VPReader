#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the VPReader project.
#
# This Source Code Form is subject to the terms of GNU GENERAL PUBLIC LICENSE Version 3, see LICENSE
# Author : Michaël Codina

from PyQt6.QtCore import QObject, pyqtSlot

class MainController(QObject):
    """ MainController(), the Controller of VPReader between MainView/FullScreenView and Model.
    """
    def __init__(self, model):
        super().__init__()
        self._model = model

    @pyqtSlot()
    def doOpenFile(self,filename):
        self._model.loadAgendaFromFile(filename)
    
    @pyqtSlot()
    def doCloseFile(self):
        self._indexItem=-1
        self._indexSlide=-1
        self._model.closeFile()

    @pyqtSlot(int)
    def itemchanged(self, value):
        #print("itemchanged "+ str(value))
        if value is not None and (value >=0 ):
            self._indexItem=value
            self._model.listSlides_changed.emit(self._model[value].getcontent())
            self._model.details_changed.emit(self._model[value].getdetails())

    @pyqtSlot(int)
    def slidechanged(self, value):
        #print("slidechanged "+ str(value))
        if (value is not None) and (value >=0 ):
            self._indexSlide=value
            self._model.preview_changed.emit(self._model[self._indexItem].getcontent()[value])

    def navigate(self, sens):
        NItems=self._model._data.__len__()
        NSlides=self._model[self._indexItem].getcontent().__len__()
        if sens=="down":
            if self._indexSlide < NSlides-1:
                self._indexSlide = self._indexSlide+1
            else:
                if self._indexItem < NItems-1: # Go black ?
                    self._indexItem = self._indexItem+1
                    self._indexSlide = 0
        else:
            if self._indexSlide > 0:
                self._indexSlide = self._indexSlide-1
            elif self._indexItem > 0: # Go black ?
                self._indexItem = self._indexItem-1
                NSlides=self._model[self._indexItem].getcontent().__len__()
                self._indexSlide = NSlides-1
        #print(str(self._indexItem) + "/" + str(NItems-1) + " : " + str(self._indexSlide) + "/" + str(NSlides-1))
        
        item=self._model[self._indexItem]

        if item.gettype()=="Song":
            #print("Song")
            self._model.fslabel_song_changed.emit(item.getcontent()[self._indexSlide])
            self._model.fsfooter_changed.emit(item.getshort())
        elif item.gettype()=="Bible":
            #print("Bible")
            self._model.fslabel_bible_changed.emit(item.getcontent()[self._indexSlide])
            self._model.fsfooter_changed.emit(item.getshort())
        elif item.gettype()=="Image":
            #print("Image")
            self._model.fslabel_image_changed.emit(self._model.dirname + item.getcontent()[self._indexSlide])
            self._model.fsfooter_changed.emit(item.getshort())