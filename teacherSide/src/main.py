#!/usr/bin/env python

from server import client_teacher
import kivy
from numpy import datetime_data

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
            print(app.teacherId,textIp.text)
        else:
            print("text empty")
    pass

    def setClassId(self, app, textIp):
        if textIp != "":
            app.classId = textIp.text.upper()
            print(app.classId,textIp.text)
        else:
            print("text empty")
    pass

class SubjectSelect(Widget):
    field_id = ObjectProperty(None)
    field_text = StringProperty(None)
    field_placeholder = StringProperty(None)

    def getText(self):
        return self.field_text

    def getPlaceHolder(self):
        return self.field_placeholder

    def setSubjectCode(self, app, textIp):
        if textIp != "":
            app.subjectId = textIp
            print(app.subjectId)
        else:
            print("text empty")
    pass


class MainWindow(Screen):
    stdTid = TeacherIdInput()
    stdTid.field_id = ObjectProperty(None)
    stdTid.field_text = 'Teacher Id:'
    stdTid.field_placeholder = 'Enter Teacher Id:'
    
    stdClass = TeacherIdInput()
    stdClass.field_id = ObjectProperty(None)
    stdClass.field_text = 'Class Id:'
    stdClass.field_placeholder = 'Enter Class Id:'

    prevColor = [1, 1, 1, 1]
    def buttonPressed(self, btn, recentUsedColor):
        self.prevColor = btn.background_color
        btn.background_color = recentUsedColor
    pass

    def exitingButtonPress(self, btn):
        btn.background_color = self.prevColor
    pass 

    pass


class SubjectSelectWindow(Screen):
    
    stdSid = SubjectSelect()
    stdSid.field_id = ObjectProperty(None)
    stdSid.field_text = 'Subject Id:'
    stdSid.field_placeholder = ''

    pass

class AttendanceControlWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class TeacherApp(App):
    teacherId =""
    classId = ""
    subjectId = ""
    
    def build(self):
        # print(type(self.winH))
        return kv

    def startAttendanceSheet(self):
        try:
            AttendanceListFromServer = client_teacher.startAttendance(self.teacherId, self.classId, self.subjectId)
            #print("started attendance with no error")
            #print(AttendanceListFromServer)
            if "error" in AttendanceListFromServer:
                print(AttendanceListFromServer["error"])
            else:
                print(AttendanceListFromServer["acode"])
                print(AttendanceListFromServer["student_list"])
                print(AttendanceListFromServer["timeout"])
        except Exception as e:
            print("error :", e)


    def updateAttendanceSheet(self):
        try:
            AttendanceListFromServer = client_teacher.getAttendance(self.teacherId,self.classId)
            #print("Refresh update list")
            #print(AttendanceListFromServer)
            if "error" in AttendanceListFromServer:
                print(AttendanceListFromServer["error"])
            else:
                print(AttendanceListFromServer["student_list"])
        except Exception as e:
            print(e)

    def finalAttendanceSheet(self):
        try:
            AttendanceListFromServer = client_teacher.stopAttendance(self.teacherId,self.classId)
            #print("Stoped attendance and got response")
            #print(AttendanceListFromServer)
            if "error" in AttendanceListFromServer:
                print(AttendanceListFromServer["error"])
            else:
                print(AttendanceListFromServer["success"])
        except Exception as e:
            print(e)


if __name__ == "__main__":
    TeacherApp().run()
