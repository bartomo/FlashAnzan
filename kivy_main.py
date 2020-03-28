#!/usr/local/bin/python3
#_*_ coding: utf-8 _*_
# author:bartomo
import os
from os.path import dirname, abspath, basename

from kivy.core.audio import SoundLoader
from kivy.core.window import Window

from kivy.clock import Clock
from decimal import Decimal, ROUND_HALF_UP

from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import StringProperty, ListProperty, ObjectProperty

# from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.uix.popup import Popup

import japanize_kivy

# resource_add_path('./IPAexfont00401')
# LabelBase.register(DEFAULT_FONT, 'mplus-2c-regular.ttf')

resource_add_path('./image')


class PopupChooseFile(BoxLayout):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    select = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MusicPlayer(BoxLayout):
    sound_path = ''
    sound = None
    popup = None
    is_playing = False
    is_pausing = False
    pause_pos = 0
    value_before = 0
    length = 0

    # audio_button = ObjectProperty(None) # > ││ボタンへのアクセス
    # status = ObjectProperty(None)
    # sound = None

    def __init__(self, **kwargs):
        print('__init__')
        super(MusicPlayer, self).__init__(**kwargs)

        self._file = Window.bind(on_dropfile=self._on_file_drop)


    def _on_file_drop(self, window, file_path):
        print('_on_file_drop')
        self.select(file_path.decode('utf-8'))
        return


    def choose(self):
        print('choose')
        content = PopupChooseFile(select=self.select, cancel=self.cancel)
        self.popup = Popup(title="Select File", content=content)
        self.popup.open()


    def play_or_stop(self):
        print('play_or_stop')
        if not self.sound:
            self.status.text = 'Select music file'
            return

        if self.sound.state == "play":
            # self.sound_position = self.sound.get_pos()
            # self.sound.stop()
            # self.audio_button.text = ">"
            # self.status.text = 'Stop {}'.format(self.sound_name)
            self._pause()

        elif self.sound.state == "stop":
            # self.sound.play()
            # self.sound.seek(self.sound_position)
            # self.audio_button.text = "││"
            # self.status.text = 'Playing {}'.format(self.sound_name)
            self._restart()
        # else:
        #     self.status.text = 'Please Select SoundFile'


    def stop(self):
        print('stop')
        if self.is_playing:
            self._stop()


    def time_change(self, value):
        if not self.sound:
            self.status.text = 'Select music file'
            return

        elif self.is_playing and value != self.value_before + 0.1:
            self._pause()
            self._restart(value)


    def volume_change(self,value):
        self._volume(value)


    def _time_string(self, now, end):
        now_m, now_s = map(int, divmod(now, 60))
        now_str = "{0}:{1:02d}".format(now_m, now_s)

        end_m, end_s = map(int, divmod(end, 60))
        end_str = "{0}:{1:02d}".format(end_m, end_s)

        return "{}/{}".format(now_str, end_str)


    def _timer(self, val):
        if not self.sound:
            return False
        elif self.time_bar.value >= self.time_bar.max:
            self._stop()
            return False

        else:
            self.value_before = self.time_bar.value
            self.time_bar.value += 0.1

            self.time_text.text = self._time_string(self.time_bar.value, self.length)


    def _volume(self, vol):
        print('_volume')
        vol = round(vol)
        vol_value = vol / 100

        self.volume_text.text = str(vol)
        self.volume_bar.value = vol

        if not self.sound:
            return

        self.sound.volume = vol_value


    def _start(self):
        print('_start')
        self.sound.play()
        self.is_playing = True
        self.is_pausing = False
        Clock.schedule_interval(self._timer, 0.1)

        self.time_bar.max = self.sound.length

        self.play_button.text = 'Interval'
        self.status.text = 'Playing {}'.format(self.sound_name)

        self.length = self.sound.length


    def _restart(self, pos=None):
        print('_restart')
        self._start()
        self.sound.seek(pos if pos else self.pause_pos)
        self.pause_pos = 0


    def _stop(self, pause=False):
        print('_stop')

        self.sound.stop()
        Clock.unschedule(self._timer)

        if not pause:
            self.is_pausing = False
            self.is_playing = False
            self.pause_pos = 0
            self.time_bar.value = 0

            self.time_text.text = self._time_string(self.time_bar.value, self.length)

        self.play_button.text = 'Play'
        self.status.text = 'Stop {}'.format(self.sound_name)


    def _pause(self):
        print('_pause')
        self.pause_pos = self.sound.get_pos()
        self._stop(True)
        self.is_pausing = True



    def cancel(self):
        print('cancel')
        self.popup.dismiss()


    def select(self, path):
        print('select')
        if self.sound:
            # self.sound.stop()
            self._stop()

        self.sound = SoundLoader.load(path)
        self.sound_path = path
        self.sound_name = basename(path)

        try:
            self._volume(50)
            self._start()
            # self.sound.play()
        except AttributeError:
            self.status.text = 'Should Sound file'
        # else:
        #     self.audio_button.text = '││'
        #     self.status.text = 'Playing {}'.format(self.sound_name)
        finally:
            if self.popup:
                self.popup.dismiss()

class ImageWidget(Widget):
    source = StringProperty('./image/sample.jpg')
    # source = StringProperty(None)

    def __init__(self, **kwargs):
        super(ImageWidget, self).__init__(**kwargs)
        pass

    def buttonClicked(self):
        self.source = './image/sample.jpg'

    def buttonClicked2(self):
        self.source = './image/sample1.jpg'

    def buttonClicked3(self):
        self.source = './image/sample2.jpg'


class TextWidget(Widget):
    text = StringProperty()
    color = ListProperty()

    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.text = ''
        self.color = [1, 1, 1, 1]

    def buttonClickedText(self):
        self.text = self.ids["text_box"].text

    def buttonClicked(self):
        self.text = 'こんにちわ'
        self.color = [1, 0 , 0, 1]

    def buttonClicked2(self):
        self.text = 'おはよう'
        self.color = [0,1,0,1]

    def buttonClicked3(self):
        self.text = 'こんばんわ'
        self.color = [0,0,1,1]


class MyWidget(GridLayout):
    def __init(self, **kwargs):
        super(GridLayout, self).__init__(**kwargs)


class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.title = "Test app"
        self.icon = "ico.png"

    def build(self):
        # return TextWidget()
        # return ImageWidget()
        # return MyWidget()
        return MusicPlayer()


def buttonClickedText():
    print("call def")
    text = 'Hello World'
    return text


if __name__ == '__main__':
    TestApp().run()

