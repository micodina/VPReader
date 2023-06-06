
from PyQt6.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QPixmap

class FullScreenView(QWidget):
    """ FullScreenWindow(QWidget) a class inherited for the FullScreen Windows.
    """
    def __init__(self, model, controller):
        super().__init__()

        self._model = model
        self._fullscreen_controller = controller
        self.setGeometry(0,0,640,480)
        self.label = QLabel(self)
        self.label.setFrameShape(QFrame.Shape.Box)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("font-size: 48pt;color: white;font-weight: bold;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.footer = QLabel(self)
        self.footer.setFrameShape(QFrame.Shape.Box)
        self.footer.setStyleSheet("font-size: 14pt;color: white;font-weight: bold;")
        self.footer.setFixedHeight(28)
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.footer)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # listen for model event signals
        self._model.fslabel_song_changed.connect(self.on_fslabel_song_changed)
        self._model.fslabel_bible_changed.connect(self.on_fslabel_bible_changed)
        self._model.fslabel_image_changed.connect(self.on_fslabel_image_changed)
        self._model.fsfooter_changed.connect(self.on_footer_changed)

    @pyqtSlot(str)
    def on_fslabel_bible_changed(self,value):
        #print("on_fslabel_changed")
        self.footer.show()
        self.setStyleSheet("background-color: grey;")
        self.label.setText(value)

    @pyqtSlot(str)    
    def on_fslabel_song_changed(self,value):
        #print("on_fslabel_song_changed")
        self.footer.show()
        self.setStyleSheet("background-color: blue;")
        self.label.setText(value)

    @pyqtSlot(str)    
    def on_fslabel_image_changed(self,value):
        #print("on_fslabel_image_changed" + value)
        self.footer.hide()
        pixmap = QPixmap(value)
        self.label.setPixmap(pixmap.scaled(self.label.size()))

    @pyqtSlot(str)    
    def on_footer_changed(self,value):
        #print("on_footer_changed")
        self.footer.setText(value)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape.value:
            self.close()
        elif event.key() == Qt.Key.Key_Up.value:
            self._fullscreen_controller.navigate("up")
        elif event.key() == Qt.Key.Key_Down.value:
            self._fullscreen_controller.navigate("down")
