#coding: utf-8
# call OpenJTalk for Windows
# sourceからコンパイルしてビルド必要
"""
クラス化モジュール化して使えるようにする
インストールフォルダをconfig.jsonから読み込むようにする
WinsoundではなくPygame.mixerを利用する
"""

import subprocess
import winsound
from datetime import datetime

class OpenJTalk(str):
    def __init__(self): #, master=None):
        str.__init__(self)
        # super().__init__(master)
        self.speed = 1

    def jtalk(t):
        # インストールフォルダ指定
        OPENJTALK_BINPATH = '/open_jtalk/bin'
        OPENJTALK_DICPATH = '/open_jtalk/dic'
        OPENJTALK_VOICEPATH = '/open_jtalk/bin/mei_normal.htsvoice'
        open_jtalk = [OPENJTALK_BINPATH + '/open_jtalk.exe']
        mech = ['-x', OPENJTALK_DICPATH]
        htsvoice = ['-m', OPENJTALK_VOICEPATH]
        speed = ['-r', '0.9']
        outwav = ['-ow', 'open_jtalk.wav']
        cmd = open_jtalk+mech+htsvoice+speed+outwav
        c = subprocess.Popen(cmd, stdin=subprocess.PIPE)

        # convert text encoding from utf-8 to shift-jis
        c.stdin.write(t.encode('shift-jis'))
        c.stdin.close()
        c.wait()

        # play wab audio file with winsound module
        winsound.PlaySound('open_jtalk.wav', winsound.SND_FILENAME)


    def say_date_time(self, msg=None):
        d = datetime.now()
        text = msg
        if msg == None:
            text = "これは　フラッシュ暗算開発用の　デフォルト オープンジェイトーク合成音声です。　現在時刻は、%s月%s日 %s時%s分%s秒です。　引数を渡してください。" % (d.month, d.day, d.hour, d.minute, d.second)
        print(text)
        OpenJTalk.jtalk(text)

    def say_question_list(self, msg=None):
        # msgにリストを渡す
        # msgのリストをstrテキストに直す
        text = "ねがいましては　"
        if msg == None:
            text = "試験問題リストがわたされていません。"
        else:
            for m in msg:
                text_que = "".join(str(m))
                # print(text_que)
                text = text+text_que
        OpenJTalk.jtalk(text)

# if __name__ == '__main__':
#     print("base_name:", os.path.basename(__file__))
#     print("dir_name:", os.path.dirname(__file__))
#
#     OpenJTalk.say_date_time()
