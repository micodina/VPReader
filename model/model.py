#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the VPReader project.
#
# This Source Code Form is subject to the terms of GNU GENERAL PUBLIC LICENSE Version 3, see LICENSE
# Author : Michaël Codina

from PySide6.QtCore import QObject, Signal
from model.VPAgenda import Song, Bible, Image

import glob
import tempfile
import zipfile
import os
import sys
import shutil
import platform


class Model(QObject):
    """ Model(), the model of VPReader used by MainView/FullScreenView and MainController.
    """
    listItems_changed = Signal(list)
    listSlides_changed = Signal(list)
    details_changed = Signal(str)
    preview_changed = Signal(str)
    selection_changed = Signal(int, int)

    fslabel_bible_changed = Signal(str)
    fslabel_song_changed = Signal(str)
    fslabel_image_changed = Signal(str)
    fsfooter_changed = Signal(str)

    def list_items(self):
        it = []
        for l in self._data:
            it.append(l.get_short())
        return (it)

    def __getitem__(self, index):
        return self._data[index]

    def load_agenda_from_file(self, newfilename):
        # print("Opening : "+ newfilename)
        self.filename = newfilename

        # Creating temp directory
        if platform.system() == 'Windows':
            self.dirname = tempfile.gettempdir()+"\\VPReader"
        else:
            self.dirname = tempfile.gettempdir()+"/VPReader"
        try:
            os.mkdir(self.dirname)
        except OSError as e:
            print("Error: %s : %s" % (self.dirname, e.strerror))

        #  .vpagd file decompression
        with zipfile.ZipFile(self.filename, 'r') as zip_ref:
            zip_ref.extractall(self.dirname)

        # Directory analysis
        agd = []
        for type in ["Song", "Bible", "Image"]:
            if platform.system() == 'Windows':
                filter = self.dirname+"\\"+type+"_*.json"
            else:
                filter = self.dirname+"/"+type+"_*.json"

            for file in glob.glob(filter):
                fn = os.path.basename(file)
                agd.append([os.stat(file).st_ino, fn, type])

        # Sort based on inode. The only way I found to get the correct order :-(
        agd.sort()

        # Populate _data[]
        self._data = []
        for item in agd:
            fn = item[1]
            type = item[2]
            index = fn[fn.find("_")+1:fn.find(".json")]
            if type == "Song":
                self._data.append(Song(self.dirname, index))
            elif type == "Bible":
                self._data.append(Bible(self.dirname, index))
            elif type == "Image":
                self._data.append(Image(self.dirname, index))

        # Display new agenda
        self.listItems_changed.emit(self.list_items())

    def close_file(self):
        self._data = []
        self.dirname = ""
        self.filename = ""
        # Remove temp directory
        try:
            shutil.rmtree(self.dirname, ignore_errors=True)
        except AttributeError:
            pass

    def __init__(self, newfilename=None):
        super().__init__()
        if newfilename == None:
            self._data = []
        else:
            self.load_agenda_from_file(newfilename)

    def __del__(self):
        # Remove temp directory
        try:
            shutil.rmtree(self.dirname, ignore_errors=True)
        except AttributeError:
            pass


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit()
    myModel = Model(sys.argv[1])
    # myModel.display()
