#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json


class Config(object):
    def __init__(self):
        config_dir = os.path.expanduser(
            "~/Library/Application Support/VPReader")
        self.config_path = os.path.join(config_dir, "VPReader.json")

        # Create configuration directery if not exists
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        # Read configuration file
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as config_file:
                self.preferences = json.load(config_file)
        else:
            self.preferences = {}
            self.preferences["directory"] = os.getenv("HOME") + "/Documents"
            self.preferences["fullscreen_bg_color"] = "blue"
            self.save()

    def save(self):
        # Save default user's preferences in configuration file
        with open(self.config_path, "w") as config_file:
            json.dump(self.preferences, config_file)
