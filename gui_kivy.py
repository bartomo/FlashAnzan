#!/usr/local/bin/python3
#_*_ coding: utf-8 _*_
# author:bartomo

# import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

from kivy.lang.builder import Builder

jpfont = 'IPAexfont00401/ipaexm.ttf'

# Builder.load_string('''
# <MainScreen>:
#     Button:
#         text: "Flash Anzan MainScreen"
#
# ''')

class MainScreen(BoxLayout):
    """
    GUIクラス
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"

        btn1 = Button(text="Show_[b]number[/b]", markup=True)
        self.add_widget(btn1)

        btn2 = Button(text="Config") # font_name=jpfont)
        self.add_widget(btn2)


        bt1 = BoxLayout()
        bt1.orientation = "horizontal"
        self.add_widget(bt1)

        btn3 = Button(text="読上開始", font_name=jpfont)
        btn4 = Button(text="[b]停止[/b]", font_size=30, font_name=jpfont, markup=True)
        bt1.add_widget(btn3)
        bt1.add_widget(btn4)

        # ti = TextInput(text="", multiline=False, font=jpfont)
        # ti.bind(on_text_validate=self.)
        # self.add_widget(ti)

        username = BoxLayout()
        username.orientation = "horizontal"
        self.add_widget(username)

        username.add_widget(Label(text="Username:", font_name=jpfont))
        username.username = TextInput(multiline=False, font_name=jpfont)
        username.add_widget(username.username)

        password = BoxLayout()
        password.orientation = "horizontal"
        self.add_widget(password)

        password.add_widget(Label(text="Password", font_name=jpfont))
        password.password = TextInput(multiline=False, font_name=jpfont)
        password.add_widget(password.password)


class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text="Username:"))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text="Password"))
        self.password = TextInput(multiline=False)
        self.add_widget(self.password)



class MainApp(App):
    """
    アプリケーションクラス
    """
    # def on_star(self):
    #     print("App start")

    def build(self):
        MS = MainScreen()
        return MS

    # def build_grid(self):
    #     return LoginScreen()

    # def on_end(self):
    #     print("Apps end")


if __name__ == "__main__":
    MainApp().run()
