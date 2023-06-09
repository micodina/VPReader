#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the VPReader project.
#
# This Source Code Form is subject to the terms of GNU GENERAL PUBLIC LICENSE Version 3, see LICENSE
# Author : Michaël Codina

import sys
from PySide6.QtWidgets import QApplication
from model.model import Model
from controllers.main_ctrl import MainController
from views.main_view import MainView
from views.fullscreen_view import FullScreenView


class App(QApplication):
    """ App(), the QApplication class, entry point of VPReader.
    """

    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()

        self.main_controller = MainController(self.model)
        self.main_view = MainView(self.model, self.main_controller)
        self.main_view.show()

        self.fullscreen_view = FullScreenView(self.model, self.main_controller)
        self.main_view.setfullscreen_view(self.fullscreen_view)


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec())
