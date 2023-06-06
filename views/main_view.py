from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import pyqtSlot, QVariant
from views.main_view_ui import Ui_MainWindow
from views.VPConfig import Config

import os
import webbrowser

class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.myConfig=Config()

        # connect widgets to controller
        self._ui.listItems.currentRowChanged.connect(self._main_controller.itemchanged)
        self._ui.listSlides.currentRowChanged.connect(self._main_controller.slidechanged)
                                                      
        # connect menu actions to controller
        self._ui.actionOpen.triggered.connect(self.doOpenFile)
        self._ui.actionClose.triggered.connect(self.doCloseFile)  
        self._ui.actionQuit.triggered.connect(self.doQuit)
        self._ui.actionFullscreen.triggered.connect(self.doFullscreen)
        self._ui.actionAbout.triggered.connect(self.doAbout)
        self._ui.actionHelp.triggered.connect(self.doHelp)

        # listen for model event signals
        self._model.listItems_changed.connect(self.on_listItems_changed)
        self._model.listSlides_changed.connect(self.on_listSlides_changed)
        self._model.details_changed.connect(self.on_details_changed)
        self._model.preview_changed.connect(self.on_preview_changed)
    
    def setfullscreen_view(self, fullscreenview):
        self._fullscreenview=fullscreenview

    @pyqtSlot(QVariant)
    def on_listItems_changed(self, value):
        #print("on_listItems_changed :" + str(value))
        for it in value:
            self._ui.listItems.addItem(it)
        self._ui.listItems.setCurrentRow(0)

    @pyqtSlot(QVariant)
    def on_listSlides_changed(self, value):
        #print("on_listSlides_changed :" + str(value))
        self._ui.listSlides.clear()
        for it in value:
            self._ui.listSlides.addItem(it)
        self._ui.listSlides.setCurrentRow(0)
    
    @pyqtSlot(str)
    def on_details_changed(self,value):
        #print("on_details_changed :" + str(value))
        self._ui.labelDetails.setText(value)

    @pyqtSlot(str)
    def on_preview_changed(self,value):
        #print("on_preview_changed :" + str(value))
        self._ui.labelPreview.setText(value)        


    def doOpenFile(self):
        fname = QFileDialog.getOpenFileName(self,  "Open File", self.myConfig.preferences["directory"], "VideoPsalm Agenda (*.vpagd);;All Files (*)")
        #fname = QFileDialog.getOpenFileName(self,  "Open File", "C:\\Users\\MYUC7345\\Documents\\Data\\Perso\\Visonneuse VideoPsalm\\Agendas EEBC\\", "VideoPsalm Agenda (*.vpagd);;All Files (*)")
        if fname[0]:
            self._main_controller.doOpenFile(fname[0])
            self.myConfig.preferences["directory"] = os.path.dirname(fname[0])
            self.myConfig.save()
            self.setWindowTitle("VPReader - " + os.path.basename(fname[0]))
    
    def doCloseFile(self):
        self._main_controller.doCloseFile()
        self._ui.listItems.clear()
        self._ui.listSlides.clear()
        self._ui.labelDetails.setText("")
        self._ui.labelPreview.setText("")
        self.setWindowTitle("VPReader")
        
    def doQuit(self):
         self.close()
    #     QApplication.quit()
         return

    def doFullscreen(self):
    #     if len(screens)>1:
    #         self.move(app.screens()[1].geometry().topLeft())
        self._fullscreenview.showFullScreen()
        #self._fullscreenview.show()
        self._main_controller.navigate("up") # à reprendre...
    #     self.fullScreenWindow.updateLabel()
    
    def doAbout(self):
        QMessageBox.information(self, "VPReader : About", "VPReader version a0.03, 5/23/2023")

    def doHelp(self):
         url="https://github.com/micodina/VPReader"
         webbrowser.open(url)

