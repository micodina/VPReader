from PyQt6.QtCore import QObject, pyqtSignal, QVariant
from model.VPAgenda import Song, Bible, Image

import glob
import tempfile
import zipfile
import os
import sys
import shutil

class Model(QObject):
    listItems_changed = pyqtSignal(QVariant)
    listSlides_changed = pyqtSignal(QVariant)
    details_changed = pyqtSignal(str)
    preview_changed = pyqtSignal(str)

    fslabel_bible_changed = pyqtSignal(str)
    fslabel_song_changed = pyqtSignal(str)
    fslabel_image_changed = pyqtSignal(str)
    fsfooter_changed = pyqtSignal(str)

    @property
    def listItems(self):
        it=[]
        for l in self._data:
            it.append(l.getshort())
        return(it)
    
    def __getitem__(self, index):
        return self._data[index]
    
    def loadAgendaFromFile(self, newfilename):
        # print("Opening : "+ newfilename)
        self.filename = newfilename
        
        # Creating temp directory
        self.dirname = tempfile.gettempdir()+"/VPReader"
        try:
            os.mkdir(self.dirname)
        except OSError as e:
            print("Error: %s : %s" % (self.dirname, e.strerror))

        #  .vpagd file decompression
        with zipfile.ZipFile(self.filename, 'r') as zip_ref:
            zip_ref.extractall(self.dirname)

        # Directory analysis
        agd=[]
        for type in ["Song","Bible","Image"]:
            for file in glob.glob(self.dirname+"/"+type+"_*.json"):
                fn=os.path.basename(file)
                agd.append([os.stat(file).st_ino,fn,type])
        
        # Sort based on inode. The only way I found to get the correct order :-(
        agd.sort()

        # Populate _data[]
        self._data=[]
        for item in agd:
            fn=item[1]
            type=item[2]
            index=fn[fn.find("_")+1:fn.find(".json")]
            if type=="Song":
                self._data.append(Song(self.dirname,index))
            elif type=="Bible":
                self._data.append(Bible(self.dirname,index))
            elif type=="Image":
                self._data.append(Image(self.dirname,index))

        # Display new agenda
        self.listItems_changed.emit(self.listItems)
        #self.fslabel_changed.emit(self._data[0].getcontent()[0])

    def closeFile(self):
        self._data=[]
        self.dirname=""
        self.filename=""
        # Remove temp directory
        try:
            shutil.rmtree(self.dirname, ignore_errors=True)
        except AttributeError:
            pass


    def __init__(self, newfilename=None):
        super().__init__()
        if newfilename==None:
            self.data=[]
        else:
            self.loadAgendaFromFile(newfilename)
    
    def __del__(self):
        # Remove temp directory
        try:
            shutil.rmtree(self.dirname, ignore_errors=True)
        except AttributeError:
            pass
        

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit()
    myModel=Model(sys.argv[1])
    #myModel.display()