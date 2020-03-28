#!/usr/local/bin/python3
#_*_ coding: utf-8 _*_
# author:bartomo

import sys
import os
import numpy as np
import tkinter as tk
import time

import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import messagebox as tkMessageBox
from tkinter import filedialog as tkFileDialog
import json
import tkinter.font as font
import exam_question
import open_jtalk
import collections as cl
import random
import threading

# 問題表示を別のモジュールにするべき
counter = 0

# アプリケーション（GUI）クラス
class Application(tk.Frame):
    DEBUG_LOG = True
    # counter = 0
    def __init__(self, master=None):
        super().__init__(master)
        self.exam_question_list = []
        # self.pack()
        self.create_widgets(self.exam_question_list)

        # self.create_widgets()

    @property
    def exam_question_list(self):
        return self._exam_question_list
    @exam_question_list.setter
    def exam_question_list(self, msg):
        self._exam_question_list = msg



    def create_widgets(self, msg='テスト'):
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
        # PanedWindow
        pw_main = tk.PanedWindow(self.master, orient='horizontal')
        pw_main.pack(expand=True, fill=tk.BOTH, side="left")

        pw_left = tk.PanedWindow(pw_main, bg="cyan", orient='vertical')
        pw_main.add(pw_left)
        pw_right = tk.PanedWindow(pw_main, bg="yellow", orient='vertical')
        pw_main.add(pw_right)

        # Frame
        fm_select = tk.Frame(pw_left, bd=2, relief="ridge")
        pw_left.add(fm_select)

        # Label
        label_fpath = tk.Label(fm_select, text="問題", width=20)
        label_fpath.grid(row=0, column=0, padx=2, pady=2)

        # Entry
        entry_fpath = tk.Entry(fm_select, justify="left", width=50)
        entry_fpath.grid(row=0, column=1, sticky=tk.W + tk.E, padx=2, pady=2)

        entry_fpath.delete(0, tk.END)
        entry_fpath.insert(0, "input your file path")

        print('Entryの初期値を出力:{}'.format(entry_fpath.get()))

        label_fpaths = tk.Label(fm_select, text="出題リスト", width=20)
        label_fpaths.grid(row=1, column=0, padx=2, pady=2)
        # Text
        selected_files = tk.Text(fm_select, height=10, width=50, wrap=tk.CHAR)
        selected_files.grid(row=1, column=1, padx=2,pady=2)

        selected_files.delete('1.0', tk.END)
        for f in range(len(msg)):
            selected_files.insert(tk.END, "{}\n".format(str(msg[f])))

        # configへの入力Entry
        f = open('config/config.json', 'r', encoding="utf-8")
        config_data = json.load(f)

        fm_config = tk.Frame(pw_left, bd=2, relief="ridge")
        fm_config.pack(side="top")
        pw_left.add(fm_config)

        label_config = tk.Label(fm_config, text="問題設定", width=20)
        label_config.grid(row=3, column=0, padx=2, pady=2)

        label_numbers = tk.Label(fm_config, text="問題数")
        label_numbers.grid(row=3, column=1, padx=2, pady=2)
        entry_numbers = tk.Entry(fm_config, justify="left", width=2)
        entry_numbers.grid(row=3, column=2, sticky=tk.W + tk.E, padx=2, pady=2)
        entry_numbers.delete(0, tk.END)
        entry_numbers.insert(0, config_data["questions_number"])

        label_terms = tk.Label(fm_config, text="項数")
        label_terms.grid(row=3, column=3, padx=2, pady=2)
        entry_terms = tk.Entry(fm_config, justify="left", width=2)
        entry_terms.grid(row=3, column=4, sticky=tk.W + tk.E, padx=2, pady=2)
        entry_terms.delete(0, tk.END)
        entry_terms.insert(0, config_data["terms_number"])

        label_lower = tk.Label(fm_config, text="下限数値")
        label_lower.grid(row=3, column=5, padx=2, pady=2)
        entry_lower = tk.Entry(fm_config, justify="left", width=2)
        entry_lower.grid(row=3, column=6, sticky=tk.W + tk.E, padx=2, pady=2)
        entry_lower.delete(0, tk.END)
        entry_lower.insert(0, config_data["digit_lower"])

        label_upper = tk.Label(fm_config, text="上限数値")
        label_upper.grid(row=3, column=7, padx=2, pady=2)
        entry_upper = tk.Entry(fm_config, justify="left", width=2)
        entry_upper.grid(row=3, column=8, sticky=tk.W + tk.E, padx=2, pady=2)
        entry_upper.delete(0, tk.END)
        entry_upper.insert(0, config_data["digit_upper"])

        set_config_list = entry_numbers.get()
        print(set_config_list)

        # configに上書きの上、問題内容を更新
        btn_config = tk.Button(fm_config, text="設定更新", command=lambda: self.btn_config_set(entry_numbers, entry_terms, entry_lower, entry_upper, config_data))
        btn_config.grid(row=3, column=9, sticky=tk.W + tk.E, padx=2, pady=2)

        # Button
        btn_select_file = tk.Button(fm_select, text="入力内容で問題更新", command=lambda: self.select_file(selected_files))
        btn_select_file.grid(row=2, column=1, sticky=tk.W + tk.E, padx=2, pady=2)

        # Buttonイベントに引数を渡す
        fm_btns = tk.Frame(pw_left, bd=2, relief="ridge")
        fm_btns.pack(side="top")
        pw_left.add(fm_btns)

        # config.jsonを読み込んで問題再生成
        btn_tool_1 = tk.Button(fm_btns, text="問題生成", command=lambda: self.btn_ivent_reset(selected_files))
        btn_tool_1.grid(row=3, column=0, sticky=tk.W + tk.E, padx=2, pady=10)

        btn_tool_2 = tk.Button(fm_btns, text="読上再生", command=lambda: self.btn_event_sound_start(self.exam_question_list))
        btn_tool_2.grid(row=3, column=1, sticky=tk.W + tk.E, padx=2, pady=10)

        # 問題表示フレーム
        print(self.exam_question_list)
        # 出題フレーム
        # exam_number_listから順に数字を表示する
        # 変更する文字を使う場合StringVar()メソッドを使う
        # exam_var = tk.StringVar()
        fm_exam = tk.Frame(pw_right, height=500, bd=2, relief="ridge")
        exam_font = font.Font(fm_exam, family="Meiryo", size=30, weight="bold")
        pw_right.add(fm_exam)
        # ここで先に表示するLabelを生成しておかないとbtn_tool3内でpackしても処理後に表示されるので見えない。
        label_exam = tk.Label(fm_exam, text="願いましては", font=exam_font)
        label_exam.pack()

        btn_tool_3 = tk.Button(fm_btns, text="問題表示", command=lambda: self.start_show_numbers(fm_exam, label_exam)) # , label_exam))
        btn_tool_3.grid(row=3, column=2, sticky=tk.W + tk.E, padx=2, pady=10)

        # タイマー表示フレーム 表示切り替えテスト用
        counter = 0
        fm_timer = tk.Frame(pw_right, bd=2, relief="ridge",)
        timer_font = font.Font(fm_timer, family="Meiryo", size=30, weight="bold")
        pw_right.add(fm_timer)
        timer001 = tk.Label(fm_timer, text="sec", font=timer_font)
        # timer001.bind('<1>', self.run(timer001))
        timer001.pack()
        btn_tool_4 = tk.Button(fm_btns, text="START", command=lambda: self.run(timer001))
        btn_tool_4.grid(row=4, column=0, sticky=tk.W + tk.E, padx=2, pady=10)

    def on_start(self, timer001):
        threading.Thread(target=self.run(timer001)).start()

    def run(self, timer001):
        # whileループつけて連続変更
        # counter = 0
        def count():
            global counter
            #for i in self.exam_question_list[0]:
            counter += 1
            timer001.config(text=str(counter))
            timer001.after(1000, count)
            print(timer001)
            print(counter)
        count()

    def start_show_numbers(self, fm_exam, label_exam): #, label_exam):
        #マルチスレッド起動しないと順表示だめか？
        print("start show numbers")
        # frame内子属性を取得し削除初期化
        children = fm_exam.winfo_children()
        for child in children:
            child.destroy()

        def run_show():
            for e in range(len(self.exam_question_list)):
            # # Label生成の部分は外に出す
            #     label_exam = {}
            #     label_exam["label_exam_{}".format(str, e)] = tk.Label(fm_exam, text="願いましては", font=exam_font)
            #     label_exam["label_exam_{}".format(str, e)].pack()

                exam_var = {}
                # exam_var["exam_var_{}".format(str, e)] = tk.StringVar()
                for num in range(len(self.exam_question_list[e])):
                    # if num > 0:
                    #     label_exam["label_exam_{}".format(str, e)].pack_forget()
                    exam_var.update({"exam_var_{}".format(e): self.exam_question_list[e][num]})
                    print(exam_var)
                    print(label_exam)
                    label_exam.configure(text="test show") # exam_var["exam_var_{}".format(str, e)])
                    # return label_exam
                    # label_exam["label_exam_{}".format(str, e)].pack()
                    # label_exam.after(1000, run)
                    time.sleep(1)
        run_show()

    def select_file(self, selected_files):
        ftyp = [("", "*.jpg;*.png")]
        iDir = os.path.abspath(os.path.dirname("__file__"))
        files = tkFileDialog.askopenfilenames(filetypes=ftyp, initialdir=iDir)

        selected_files.delete('1.0', tk.END)
        file_list = list(files)
        # if (len(file_list) <= 10):
        for i in np.arange(0, len(file_list)):
            selected_files.insert("end", "{}\n".format(file_list[i]))
        print(file_list)
        self.show_image(file_list[0])

    def show_image(self, file_path):
        w, h = 500, 500
        image = Image.open(file_path)
        image = image.resize((w, h), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        self.panel_img.configure(image=self.img)
        self.panel_img.pack()

    def change_panel(self, fm_exam, exam_font, e): # , exam_var):
        label_exam = {}
        label_exam["label_exam_{}".format(e)] = tk.Label(fm_exam, text="願いましては", font=exam_font)
        label_exam["label_exam_{}".format(e)].pack()
        exam_var = {}
        exam_var["exam_var_{}".format(e)] = tk.StringVar()
        for num in range(len(self.exam_question_list[e])):
            if num > 0:
                label_exam["label_exam_{}".format(e)].pack_forget()
            exam_var["exam_var_{}".format(e)].set(self.exam_question_list[e][num])
            # label_exam["label_exam_{}".format(str, e)] = tk.Label(fm_exam, textvariable=exam_var["exam_var_{}".format(str, e)], font=exam_font)
            label_exam["label_exam_{}".format(e)]["text"] = exam_var["exam_var_{}".format(e)]
            # return label_exam
            # label_exam["label_exam_{}".format(str, e)].pack()
            time.sleep(1)
            # label_exam.pack_forget()
            # label_exam.bind("<button_change>", change_next_num)

    def change_next_num(event):
        strings = random.choice(["A", "B", "C"])
        var = tk.StringVar
        var.set("Hello")
        var_label = tk.Label()

    def img_click(self, ev):
        print('クリックされた位置：x {}、y {}'.format(ev.x, ev.y))

    def btn_ivent_reset(self, selected_files):
        """
        exam_questionを呼び出して問題再生成
        tk.Textオブジェクトselected_filesを消してexamquestion_listを再描画
        :param msg:
        :return:
        """
        print("reset_exam_question_list")

        msg_que = exam_question.ExamQuestion()
        msg_que.set_config()
        msg = msg_que.create_exam_question()
        # exam_number_list = exam_question.ExamQuestion()
        # exam_number_list.set_config()
        # myapp.exam_question_list = exam_number_list.create_exam_question()

        # selected_files = tk.Text(fm_select, height=10, width=50, wrap=tk.CHAR)
        # selected_files.grid(row=1, column=1, padx=2,pady=2)

        selected_files.delete('1.0', tk.END)
        # selected_files.insert(tk.END, "No.1 file path\n")
        # selected_files.insert(tk.END, "No.2 file path\n")
        for f in range(len(msg)):
            selected_files.insert(tk.END, "{}\n".format(str(msg[f])))

        self.exam_question_list = msg
        return self.exam_question_list

    def btn_ivent_get(self, msg):
        print(msg)

    def btn_config_set(self, numbers, terms, lower, upper, config_data):
        """
        config内容をEntry入力内容で上書きして
        exam_questionで問題内容を再生成
        表示内容を更新する
        :param msg:
        :return: config_data
        """
        config_set = open('config/config.json', 'w', encoding="utf-8")
        # config_set = json.load(f)
        # config_set_str = json.dumps(config_set)
        # print("元：" + config_set_str)

        config_data["questions_number"] = numbers.get()
        config_data["terms_number"] = terms.get()
        config_data["digit_lower"] = lower.get()
        config_data["digit_upper"] = upper.get()
        # config_data_str = json.dumps(config_data)
        print("修正：" + str(config_data))
        json.dump(config_data, config_set, indent=4)
        return config_data

    def btn_event_sound_start(self, msg):
        """
        Textの内容をgetしてOpneJtalk再生
        :param msg:
        :return:
        """
        voice = open_jtalk.OpenJTalk()
        print("読上げ速度:" + str(voice.speed))
        voice.say_question_list(msg)

    def btn_event_sound_stop(self, msg):
        """
        winsound.SND_PURGEでは現在停止できない
        winsoundからPygameに修正する
        :param msg:
        :return:
        """
        pass
