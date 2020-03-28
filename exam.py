#!/usr/local/bin/python3
#_*_ coding: utf-8 _*_
# author:bartomo
# フラッシュ暗算メイン実行ファイルとして以下のモジュールを実行
# 問題作成モジュール：exam_question.py
# GUIモジュール：create_widgets.py
# 音声出力モジュール：open_jtalk.py
# 設定：config.json

import os, sys
import create_widgets
import exam_question
import open_jtalk
import tkinter as tk

if __name__ == "__main__":
    print("main running")
    root = tk.Tk()
    myapp = create_widgets.Application(master=root)
    myapp.master.title("Flash暗算 ver0.0.2")
    myapp.master.geometry("1000x600")

    exam_number_list = exam_question.ExamQuestion()
    exam_number_list.set_config()
    myapp.exam_question_list = exam_number_list.create_exam_question()

    myapp.mainloop()

