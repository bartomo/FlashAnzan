﻿#!/usr/local/bin/python3
#_*_ coding: utf-8 _*_
# author:bartomo

from os.path import dirname, abspath
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class PopupChooseFile(BoxLayout):
    current_dir = dirname(abspath(__file__))

    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

