#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import tempfile
import re
import json
import zipfile
import os

def readSongFromFile(fichier):
        # Open file in read-only
        with open(fichier, 'r') as f:
            # Read data
            data = f.read()
        
        # Encoding correction
        data=data.encode().decode('utf-8-sig')

        # Keys format correction
        data=re.sub("Abbreviation:","\"Abbreviation\":",data)
        data=re.sub("Songs:","\"Songs\":",data)
        data=re.sub("Composer:","\"Composer\":",data)
        data=re.sub("Author:","\"Author\":",data)
        data=re.sub("Copyright:","\"Copyright\":",data)
        data=re.sub("Reference:","\"Reference\":",data)
        data=re.sub("Guid:","\"Guid\":",data)
        data=re.sub("Verses:","\"Verses\":",data)
        data=re.sub("Text:","\"Text\":",data)
        data=re.sub("Tag:","\"Tag\":",data)
        data=re.sub("ID:","\"ID\":",data)
        data=re.sub("VersionDate:","\"VersionDate\":",data)
        data=re.sub("Theme:","\"Theme\":",data)
        data=re.sub("VideoDuration:","\"VideoDuration\":",data)

        # Parsing json
        data=json.loads(data,strict=False)

        return(data)


def readAgendaFromFile(fichier):
    # Creating temp directory
    dirname=tempfile.gettempdir()+"/VPReader"
    try:
        os.mkdir(dirname)
    except OSError as e:
            print("Error: %s : %s" % (dirname, e.strerror))

    #  .vpagd file decompression
    with zipfile.ZipFile(fichier, 'r') as zip_ref:
        zip_ref.extractall(dirname)
    
    # Directory analysis
    data=[]
    i=0
    while True:
        myfic=dirname+"/Song_"+str(i)+".json"
        if not(os.path.isfile(myfic)):
             break
        print("Je lis " + myfic)
        data.append(readSongFromFile(myfic))
        i=i+1

    # Remove temp directory
    files = glob.glob(dirname+'/*')
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
    os.rmdir(dirname)
        # Une liste de song
        # Une song est un dictionnaire... clefs : ID (n°), Text(Titre) et Verses (+ Composer,Author,Copyright,Reference,Guid et VideoDuration)
        # Verses est un dictionnaire... clefs : Tag, Text    
    return data


class Agenda(object):
    def __init__(self, newfilename):
        print("J'ouvre : "+ newfilename)
        self.filename=newfilename
        self.songs=readAgendaFromFile(newfilename)

#    def __del__(self):
