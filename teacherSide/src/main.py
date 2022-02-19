#!/usr/bin/env python

import abc
from server import client_teacher
import kivy
from numpy import datetime_data

import os
import imp
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.label import Label
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

''' ############################# classes for various data to and fro from kv and python side ############################### '''
#teacher id input class
class TeacherIdInput(Widget):
    field_id = ObjectProperty(None)
    field_text = StringProperty(None)
    field_placeholder = StringProperty(None)
    
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

#subject id selection class
class SubjectSelect(Widget):
    field_id = ObjectProperty(None)
    field_text = StringProperty(None)

    def setSubjectCode(self, app, textIp):
        if textIp != "":
            app.subjectId = textIp
            print(app.subjectId)
        else:
            print("text empty")
    pass
    
    
#attendance code class
class AttendanceDetail(Widget):
    field_AttendanceId = StringProperty(None)
    field_teacherId = StringProperty(None)
    field_classId = StringProperty(None)
    field_subjectId = StringProperty(None)
    pass

''' ############################################### Classes for kivy windows ############################################### '''
class MainWindow(Screen):
    stdTid = TeacherIdInput()
    stdTid.field_id = ObjectProperty(None)
    stdTid.field_text = 'Teacher Id:'
    stdTid.field_placeholder = 'Example : 011'

    stdClass = TeacherIdInput()
    stdClass.field_id = ObjectProperty(None)
    stdClass.field_text = 'Class Id:'
    stdClass.field_placeholder = 'Example : 075BCTCD'

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
    pass

    def startAttendanceSheet(self):
        try:
            AttendanceListFromServer = client_teacher.startAttendance(self.teacherId, self.classId, self.subjectId)
            if "error" in AttendanceListFromServer:
                print(AttendanceListFromServer["error"])
            else:
                #save attendance code
                TeacherApp.attendanceId = AttendanceListFromServer["acode"]
                for list in AttendanceListFromServer["student_list"]:
                    print(list[0], list[1])
                print(AttendanceListFromServer["timeout"])
                print(TeacherApp.attendanceId)
        except Exception as e:
            print("error :", e)

class AttendanceControlWindow(Screen):
    attendanceInstance = AttendanceDetail()        
    attendanceInstance.field_AttendanceId = 'No attendance code'
    
    def updateAttendanceSheet(self):
        try:
            AttendanceListFromServer = client_teacher.getAttendance(self.teacherId,self.classId)
            if "error" in AttendanceListFromServer:
                print(AttendanceListFromServer["error"])
            else:
                print(AttendanceListFromServer["student_list"])
        except Exception as e:
            print(e)

    def finalAttendanceSheet(self):
        try:
            AttendanceListFromServer = client_teacher.stopAttendance(self.teacherId,self.classId)
            if "error" in AttendanceListFromServer:
                print(AttendanceListFromServer["error"])
            else:
                print(AttendanceListFromServer["success"])
        except Exception as e:
            print(e)
''' ############################################### Kivy App builder ################################################ '''
class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")


class TeacherApp(App):
    teacherId =""
    classId = ""
    subjectId = ""
    attendanceId =""
    
    def build(self): 
        return kv

if __name__ == "__main__":
    TeacherApp().run()
