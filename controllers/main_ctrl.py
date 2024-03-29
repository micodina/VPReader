#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the VPReader project.
#
# This Source Code Form is subject to the terms of GNU GENERAL PUBLIC LICENSE Version 3, see LICENSE
# Author : Michaël Codina

from PySide6.QtCore import QObject, Slot


class MainController(QObject):
    """ MainController(), the Controller of VPReader between MainView/FullScreenView and Model.
    """

    def __init__(self, model):
        super().__init__()
        self._model = model
        self._current_item = -1
        self._current_slide = -1
        self._black = False

    @Slot()
    def do_open_file(self, filename):
        self._model.load_agenda_from_file(filename)
        self._model.listItems_changed.emit(self._model.list_items())

    @Slot()
    def do_close_file(self):
        self._current_item = -1
        self._current_slide = -1
        self._model.close_file()

    @Slot(int)
    def item_changed(self, value):
        """
        Slot déclenché par le signal currentRowChanged du QListWidget ListItems.
        Méthode appelée par jump().
        """
        print("item_changed "+ str(value))
        if value is not None and (value >= 0):
            self._current_item = value
            item=self._model[value]
            self._model.listSlides_changed.emit(item.get_content())
            self._model.details_changed.emit(item.get_details())

    @Slot(int)
    def slide_changed(self, value):
        """
        Slot déclenché par le signal currentRowChanged du QListWidget ListSlides.
        Méthode appelée par jump().
        """
        print("slide_changed "+ str(value))
        if (self._current_item >= 0) and (value is not None) and (value >= 0):
            self._current_slide = value
            item = self._model[self._current_item]
            slides=item.get_content()

            # Update MainView()
            self._model.preview_changed.emit(slides[self._current_slide])

            # Update FullScreenView()
            if item.get_type() == "Song":
                # print("Song")
                self._model.fslabel_song_changed.emit(slides[self._current_slide])
                self._model.fsfooter_changed.emit(item.get_short())
            elif item.get_type() == "Bible":
                # print("Bible")
                self._model.fslabel_bible_changed.emit(slides[self._current_slide])
                self._model.fsfooter_changed.emit(item.get_short())
            elif item.get_type() == "Image":
                # print("Image")
                self._model.fslabel_image_changed.emit(self._model.dirname + slides[self._current_slide])
                self._model.fsfooter_changed.emit(item.get_short())
            elif item.get_type() == "Pdf":
                #print("Pdf")
                self._model.fspdfview_changed.emit(item.get_filename(), self._current_slide )

    def jump(self, sens):
        # Default turn black screen
        # if not (self._black):
        #     # print("Black")
        #     self._black = True
        #     self._model.fslabel_black_changed.emit()
        #     return
        # self._black = False
        # print("Jump")
        # After black screen, do a jump
        if sens == "down":
            # Not the last item ?
            if self._current_item < len(self._model)-1:
                self._current_item += 1
                self.item_changed(self._current_item)
                self._model.selection_item_changed.emit(self._current_item)
        else:
            # Not the first item ?
            if self._current_item > 0:
                self._current_item -= 1
                item=self._model[self._current_item]
                self.item_changed(self._current_item)
                self.slide_changed(len(item.get_content())-1)
                self._model.selection_item_changed.emit(self._current_item)
                self._model.selection_slide_changed.emit(len(item.get_content())-1)
