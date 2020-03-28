#!/usr/local/bin/python3
#_*_ coding: utf-8 _*_
# author:bartomo

import os
from os.path import basename
import japanize_kivy

from kivy.app import App

from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')

from musicplayer import MusicPlayer
from exam_question import ExamQuestion

class ExamApp(App):
    def __init__(self, **kwargs):
        super(ExamApp, self).__init__(**kwargs)
        self.title = "Flash"
        self.icon = "ico.png"
        self.exam_quextion_list = []
        exam_number_list = ExamQuestion()
        exam_number_list.set_config()
        print(exam_number_list)

    def build(self):
        return MusicPlayer()


def buttonClickedText():
    print("call def")
    text = 'Hello World'
    return text


if __name__ == '__main__':
    ExamApp().run()

