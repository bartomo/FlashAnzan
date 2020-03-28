#!/usr/local/bin/python3
#_*_ coding: utf-8 _*_

from os.path import basename

from kivy.core.audio import SoundLoader
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from kivy.clock import Clock
from decimal import Decimal, ROUND_HALF_UP

from popupchooser import PopupChooseFile

from exam_question import ExamQuestion
import json


class MusicPlayer(BoxLayout):
    sound_path = ''
    sound = None
    popup = None
    is_playing = False
    is_pausing = False
    pause_pos = 0
    value_before = 0
    length = 0


    def __init__(self, **kwargs):
        print('__init__')
        super(MusicPlayer, self).__init__(**kwargs)

        self._file = Window.bind(on_dropfile=self._on_file_drop)

        # self.exam_number_list = []
        # exam_number_list = ExamQuestion()
        # exam_number_list.set_config()
        # print(exam_number_list.create_exam_question())
        self._create_number_list()


    def _create_number_list(self):
        """
        create_widgets.btn_ivent_resetを移植
        if文で初回問題が生成されてるかチェックできる
        :return:
        """
        self.exam_number_list = []
        exam_number_list = ExamQuestion()
        exam_number_list.set_config()
        print(exam_number_list.create_exam_question())
        self.status.text = "exam_number_list"



    def _start_show_number(self):
        """
        exam_number_listを順に表示
        :return:
        """
        pass


    def _set_exam_config(self):
        """
        btn_config_setを移植
        :return:
        """
        pass


    def _open_jtalk(self):
        """
        WAVファイル生成してreturnするメソッド追加
        :return:
        """
        pass


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
            # self.exam_number.text = 'test play'
            return

        if self.sound.state == "play":
            self._pause()

        elif self.sound.state == "stop":
            self._restart()


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
        # self.exam_number.text = 'test show number'

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
            self._stop()

        self.sound = SoundLoader.load(path)
        self.sound_path = path
        self.sound_name = basename(path)

        try:
            self._volume(50)
            self._start()
        except AttributeError:
            self.status.text = 'Should Sound file'
        finally:
            if self.popup:
                self.popup.dismiss()

