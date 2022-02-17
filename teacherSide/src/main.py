#!/usr/bin/env python
import kivy
from numpy import datetime_data

import server.client_teacher
import os
import imp
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty,ObjectProperty
from kivy.utils import platform
from kivy.clock import mainthread
from kivy.logger import Logger

class TeacherIdInput(Widget):
    field_id = ObjectProperty(None)
    field_text = StringProperty(None)
    field_placeholder = StringProperty(None)

    def getText(self):
        return self.field_text

    def getPlaceHolder(self):
        return self.field_placeholder

    def setTeacherId(self, app, textIp):
        if textIp != "":
            app.teacherId = textIp.text
            #print(app.teacherId,textIp.text)
        else:
            print("text empty")
    pass


class MainWindow(Screen):
    stdTid = TeacherIdInput()
    stdTid.field_id = ObjectProperty(None)
    stdTid.field_text = 'Teacher Id:'
    stdTid.field_placeholder = 'Enter Teacher Id:'
    
    prevColor = [1, 1, 1, 1]
    def buttonPressed(self, btn, recentUsedColor):
        self.prevColor = btn.background_color
        btn.background_color = recentUsedColor

    def exitingButtonPress(self, btn):
        btn.background_color = self.prevColor

    pass


class ClassSelectWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class TeacherApp(App):
    # winH = NumericProperty(Window.size[0])
    # winW = NumericProperty(Window.size[1])

    def build(self):
        # print(type(self.winH))
        return kv

    # def buttonPressed(self):
    #     print("Change buttton color for a second?")


if __name__ == "__main__":
    TeacherApp().run()
