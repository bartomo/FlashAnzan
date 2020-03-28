#!/usr/local/bin/python3
#_*_ coding: utf-8 _*_
# author:bartomo

import random
import numpy
import os, sys, time
import json
import tkinter as tk
import create_widgets
import open_jtalk


class ExamQuestion(list):
    """
    ExamQuestion基底クラスオブジェクト
    list型
    configオブジェクトから設定変数を読み取り出題する問題を生成して返します。
    :param :
    :return:
    """
    def __init__(self):
        """


        """
        list.__init__(self)
        f = open('config/config.json', 'r', encoding="utf-8")
        config = json.load(f)
        self._questions_number = 1
        self._terms_number = 2
        self._digit_lower = 1
        self._digit_upper = 9

    # @propertyを使って属性セットすることで開発上意図しない読み書きを防ぐことになる。
    @property
    def questions_number(self):
        return self._questions_number
    @questions_number.setter
    def questions_number(self, val):
        self._questions_number = val

    @property
    def terms_number(self):
        return self._terms_number
    @terms_number.setter
    def terms_number(self, val):
        self._terms_number = val

    @property
    def digit_lower(self):
        return self._digit_lower
    @digit_lower.setter
    def digit_lower(self, val):
        self._digit_lower = val

    @property
    def digit_upper(self):
        return self._digit_upper
    @digit_upper.setter
    def digit_upper(self, val):
        self._digit_upper = val

    def set_config(self):
        # formatで入れ込み
        f = open('config/config.json', 'r', encoding="utf-8")
        config = json.load(f)
        self.questions_number = config["questions_number"]
        self.terms_number = config["terms_number"]
        self.digit_lower = config["digit_lower"]
        self.digit_upper = config["digit_upper"]
        conf = "問題数：{} / 項数：{} / 下限：{} /上限：{}".format(self.questions_number, self.terms_number, self.digit_lower, self.digit_upper)
        print(conf)
        return self

    def create_number_list(self):
        """
        Config設定を読み込みRandom問題リストを作成
        :param self:
        :return exam_number_list
        """
        # 出題数のリスト　questions_number
        # 項数のリスト terms_number
        # 出題桁数の制限変数 digit_upper,digit_lower
        # 数字のリスト number_list
        exam_number_list = []
        for q in range(1, int(self.questions_number) + 1):
            exam_que = []
            for t in range(1, int(self.terms_number)+1):
                exam_que.append(random.randint(int(self.digit_lower), int(self.digit_upper)))
            exam_number_list.append(exam_que)
        # print(exam_number_list)
        return exam_number_list

    def create_operator_list(self):
        """
        Config設定を読み込み加減乗除の演算子listを作成
        :param terms_number:
        :param questions_number:
        :param self:question_number, terms_number
        :return:exam_operator_list
        """
        global operator_que
        operator = ["+", "ひく", "×", "÷"]
        exam_operator_list = []
        for o in range(1, int(self.questions_number) + 1):
            operator_que = []
            for q in range(1, int(self.terms_number)):
                random.shuffle(operator)
                operator_que.append(operator[0])
            exam_operator_list.append(operator_que)
        # print(exam_operator_list)
        return exam_operator_list

    def create_exam_question(self):
        """
        exam_number_listから問題を作成

        :param self:
        :return: exam_question_list
        """
        global question_number_que, question_operator_que, exam_question_list, exam_question_que

        question_number_que = self.create_number_list()
        question_operator_que = self.create_operator_list()
        exam_question_list = []
        for n in range(len(question_number_que)):
            exam_question_que = [None] * (len(question_number_que[0]) + len(question_operator_que[0]))
            exam_question_que[::2] = question_number_que[n]
            exam_question_que[1::2] = question_operator_que[n]
            exam_question_list.append(exam_question_que)
        return exam_question_list

    def answer_list(self):
        """
        exam
        :param self:
        :return:
        """

    def exam_run(self): """
        exam_question_listを受け取って問題表示
        :param self:
        :return:
        """

    def answer(self):
        """

        :param self:
        :return:
        """

    def pushed(self):
        print("clicked")
        self["text"] = "回答済み"

if __name__ == "__main__":
    # global question_number_que, question_operator_que, exam_question_list, exam_question_que

    print("main running")
    # exam_number_listにConfig設定を読み込んで引数にする処理
    # ExamQuestionクラスのインスタンス　問題の設定生成を持つオブジェクト
    exam_number_list = ExamQuestion()
    exam_number_list.set_config()
    exam_number_list.create_exam_question()

    # preview
    # print(exam_question_list)
    for p in range(len(exam_question_list)):
        exam = ''.join(map(str, exam_question_list[p]))
        print('問題'+str(p+1)+': '+exam+"=")

    # TkinterでGUI表示
    def pushed(self):
        print("clicked")
        self["text"] = "回答済み"


    # for p in range(len(exam_question_list)):
      #  exam = ''.join(map(str, exam_question_list[p]))
      #  label1 = tk.Label(root1, text='問題{}: {}='.format(p, exam))
      #  label1.grid()

    root = tk.Tk()
    myapp = create_widgets.Application(master=root)
    myapp.master.title("Flash暗算 ver0.0.1")  # タイトル
    myapp.master.geometry("1000x600")  # ウィンドウの幅と高さピクセル単位で指定

    # myappにexam_question_listを引き渡せてるかテスト
    myapp.exam_question_list = exam_question_list
    # myapp.create_widgets(exam_question_list)
    myapp.create_widgets(exam_question_list)

    # myapp.mainloop()

    # creatte_widgetsにquestion_listを引き渡して描画
    # create_widgetsのEntryからconfig.jsonに読み書き変更
    # create_widgetsのTextからexam_question_listの内容書き換え

    # create_widgetsの実行ButtonでOpenJtalkにexam_question_listからテキスト生成して実行
    # OpenJtalk読上げクラステスト
    voice = open_jtalk.OpenJTalk()
    print("読上げ速度:"+ str(voice.speed))
    voice.say_question_list(exam_question_list)

    myapp.mainloop()


