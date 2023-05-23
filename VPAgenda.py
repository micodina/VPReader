#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the VPReader project.
#
# This Source Code Form is subject to the terms of GNU GENERAL PUBLIC LICENSE Version 3, see LICENSE
# Author : Michaël Codina

import glob
import tempfile
import re
import json
import zipfile
import os
import sys
import shutil

   

def keysformat(ch):
    keys=("Abbreviation", "Administrator", "Author", "AutoAdvance", "Background", "Body", "BodyRect", "Bold", "Books", "Brush", "CaseType", "Chapters", "Chords", "Color", "Composer", "Copyright", "Description", "EndPosition", "Fill", "FileName", "FontName", "FontSize", "FontStyle", "Footer", "FooterRect", "Guid", "Header", "HeaderRect", "HiddenSlides", "ID", "Image", "Interval", "Introduction", "IsCompressed", "IsLooping", "IsMuted", "IsProtected", "Italic", "Language", "Luminosity", "Memo1", "Publisher", "Reference", "RotateFlipType", "Sequence", "Songs", "Source", "StartPosition", "Stretch", "Stroke", "Tag", "Style", "Template", "Testaments", "Text", "TextAlignment", "Theme", "Transition", "Type", "Underlined", "UseCurrentLanguage", "Verses", "VersionDate", "VerticalAlignment", "VideoDuration", "Volume", "Wrap", "Duration")
    for k in keys:
        ch=re.sub(k+':','"' + k + '":', ch)
    return(ch)


def readJsonFile(fichier):
    # Open file in read-only
    with open(fichier, 'r') as f:
        # Read data
        data = f.read()

    # Encoding correction
    data = data.encode().decode('utf-8-sig')

    # Keys format correction
    data=keysformat(data)

    # Parsing json
    data = json.loads(data, strict=False)

    # Lot of json files owned an array called "Verses" of dict with no "ID" key
    if "Verses" in data.keys() : 
        for i in data["Verses"]:
            if i.get("ID") is None:
                i.update({"ID":1})

    return (data)


class Item():
    """ Item(), an abstract class of item.
    Items are songs, biblical texts or images.
    """
    def display(self):
        print(self.getshort())
        print(self.getcontent())

class Song(Item):
    """ Song(), a class inherited from item dedicated for Songs.
    """
    def __init__(self, dirname, index):
        self.data=readJsonFile(dirname + "/Song_" + index + ".json" )
        self.songbook=readJsonFile(dirname + "/SongBook_" + index + ".json" )

    def getshort(self):
        sh=""
        if "ID" in self.data.keys():
            sh=str(self.data["ID"])
        if "Text" in self.data.keys():
            sh=sh + " " + self.data["Text"]
        return(sh)
    
    def getcontent(self):
        return(self.data["Verses"])
    
    def gettype(self):
        return("Song")

class Bible(Item):
    """ Bible(), a class inherited from item dedicated for biblical texts.
    """
    def __init__(self, dirname, index):
        self.data=readJsonFile(dirname + "/BibleVerses_" + index + ".json" )
        self.biblebook=readJsonFile(dirname + "/BibleBook_" + index + ".json" )
        self.biblechapter=readJsonFile(dirname + "/BibleChapter_" + index + ".json" )

    def getshort(self):
        min=1000
        max=0
        for i in self.data["Verses"]:
            if i.get("ID") is not None:
                if i["ID"]>max:
                    max=i["ID"]
                if i["ID"]<min:
                    min=i["ID"]
        return("{} {}.{}-{}".format(self.biblebook["Abbreviation"],self.biblechapter["ID"], min, max))
    
    def getcontent(self):
        return(self.data["Verses"])
    
    def gettype(self):
        return("Bible")

class Image(Item):
    """ Image(), a class inherited from item dedicated for Images.
    """
    def __init__(self, dirname, index):
        self.data=readJsonFile(dirname + "/Image_" + index + ".json" )

    def getshort(self):
        return(self.data["Text"])
    
    def getcontent(self):
        fn=self.data["FileName"].replace('\\','/')[2::]
        return([{'Text': fn },])
    
    def gettype(self):
        return("Image")
    
class Agenda(object):
    """ Agenda(), a class container of the content of a VideoPsalm© agenda.
        Constructor optionaly read a file and decompress it in a temp directory.
        self.display() allows a basic rendering of the content of an agenda.
    """
    def __init__(self, newfilename=None):
        if newfilename==None:
            self.data=[]
            return
        
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

        self.data=[]
        for item in agd:
            fn=item[1]
            type=item[2]
            index=fn[fn.find("_")+1:fn.find(".json")]
            if type=="Song":
                self.data.append(Song(self.dirname,index))
            elif type=="Bible":
                self.data.append(Bible(self.dirname,index))
            elif type=="Image":
                self.data.append(Image(self.dirname,index))

    def display(self):
        print("Agenda : {}, décompressed in : {}".format(self.filename, self.dirname) )
        for obj in self.data:
            print(obj.gettype())
            obj.display()

    def __del__(self):
        # Remove temp directory
        try:
            shutil.rmtree(self.dirname, ignore_errors=True)
        except AttributeError:
            pass

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit()
    myAgenda=Agenda(sys.argv[1])
    myAgenda.display()
