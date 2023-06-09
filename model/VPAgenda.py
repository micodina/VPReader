#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the VPReader project.
#
# This Source Code Form is subject to the terms of GNU GENERAL PUBLIC LICENSE Version 3, see LICENSE
# Author : Michaël Codina

import re
import json
import platform


def keys_format(ch):
    keys = ("Abbreviation", "Administrator", "Author", "AutoAdvance", "Background", "Body", "BodyRect", "Bold", "Books", "Brush", "CaseType", "Chapters", "Chords", "Color", "Composer", "Copyright", "Description", "EndPosition", "Fill", "FileName", "FontName", "FontSize", "FontStyle", "Footer", "FooterRect", "Guid", "Header", "HeaderRect", "HiddenSlides", "ID", "Image", "Interval", "Introduction", "IsCompressed", "IsLooping",
            "IsMuted", "IsProtected", "Italic", "Language", "Luminosity", "Memo1", "Publisher", "Reference", "RotateFlipType", "Sequence", "Songs", "Source", "StartPosition", "Stretch", "Stroke", "Tag", "Style", "Template", "Testaments", "Text", "TextAlignment", "Theme", "Transition", "Type", "Underlined", "UseCurrentLanguage", "Verses", "VersionDate", "VerticalAlignment", "VideoDuration", "Volume", "Wrap", "Duration")
    for k in keys:
        ch = re.sub(k+':', '"' + k + '":', ch)
    return (ch)


def read_json_file(fichier):
    # Open file in read-only
    # with open(fichier, 'r') as f:
    with open(fichier, 'r', encoding="utf8") as f:
        # Read data
        data = f.read()

    # Encoding correction
    data = data.encode().decode('utf-8-sig')

    # Keys format correction
    data = keys_format(data)

    # Parsing json
    data = json.loads(data, strict=False)

    # Lot of json files owned an array called "Verses" of dict with no "ID" key
    if "Verses" in data.keys():
        for i in data["Verses"]:
            if i.get("ID") is None:
                i.update({"ID": 1})

    return (data)


class Item():
    """ Item(), an abstract class of item.
    Items are songs, biblical texts or images.
    """

    def display(self):
        print(self.get_short())
        print(self.get_content())

    def get_details(self):
        return ("My details")


class Song(Item):
    """ Song(), a class inherited from item dedicated for Songs.
    """

    def __init__(self, dirname, index):
        if platform.system() == 'Windows':
            self.data = read_json_file(dirname + "\\Song_" + index + ".json")
            self.songbook = read_json_file(
                dirname + "\\SongBook_" + index + ".json")
        else:
            self.data = read_json_file(dirname + "/Song_" + index + ".json")
            self.songbook = read_json_file(
                dirname + "/SongBook_" + index + ".json")

    def get_short(self):
        sh = ""
        if "ID" in self.data.keys():
            sh = str(self.data["ID"])
        if "Text" in self.data.keys():
            sh = sh + " " + self.data["Text"]
        return (sh)

    def get_content(self):
        co = []
        for i in self.data["Verses"]:
            co.append(i["Text"])
        return (co)

    def get_details(self):
        de = ""
        for k in ["Abbreviation", "Description", "Publisher", "Copyright", "Text"]:
            if k in self.songbook.keys():
                de = de + "\n" + k + ":" + self.songbook[k]
        return (de)

    def get_type(self):
        return ("Song")


class Bible(Item):
    """ Bible(), a class inherited from item dedicated for biblical texts.
    """

    def __init__(self, dirname, index):
        if platform.system() == 'Windows':
            self.data = read_json_file(
                dirname + "\\BibleVerses_" + index + ".json")
            self.biblebook = read_json_file(
                dirname + "\\BibleBook_" + index + ".json")
            self.biblechapter = read_json_file(
                dirname + "\\BibleChapter_" + index + ".json")
        else:
            self.data = read_json_file(
                dirname + "/BibleVerses_" + index + ".json")
            self.biblebook = read_json_file(
                dirname + "/BibleBook_" + index + ".json")
            self.biblechapter = read_json_file(
                dirname + "/BibleChapter_" + index + ".json")

    def get_short(self):
        min = 1000
        max = 0
        for i in self.data["Verses"]:
            if i.get("ID") is not None:
                if i["ID"] > max:
                    max = i["ID"]
                if i["ID"] < min:
                    min = i["ID"]
        return ("{} {}.{}-{}".format(self.biblebook["Abbreviation"], self.biblechapter["ID"], min, max))

    def get_content(self):
        co = []
        for i in self.data["Verses"]:
            co.append(i["Text"])
        return (co)

    def get_details(self):
        de = ""
        for k in ["Abbreviation", "Introduction", "Publisher", "Copyright", "Text"]:
            if k in self.biblebook.keys():
                de = de + "\n" + k + ":" + self.biblebook[k]
        return (de)

    def get_type(self):
        return ("Bible")


class Image(Item):
    """ Image(), a class inherited from item dedicated for Images.
    """

    def __init__(self, dirname, index):
        if platform.system() == 'Windows':
            self.data = read_json_file(dirname + "\\Image_" + index + ".json")
        else:
            self.data = read_json_file(dirname + "/Image_" + index + ".json")

    def get_short(self):
        return (self.data["Text"])

    def get_content(self):
        fn = self.data["FileName"].replace('\\', '/')[2::]
        return ([fn,])

    def get_details(self):
        return (self.data["Text"])

    def get_type(self):
        return ("Image")
