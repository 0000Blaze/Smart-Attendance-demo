#!/usr/bin/env python
import GlobalShared
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
            #print(app.teacherId,textIp.text)
            GlobalShared.teacherId = app.teacherId
            print(GlobalShared.teacherId)
        else:
            print("text empty")
    pass
    def setClassId(self, app, textIp):
        if textIp != "":
            app.classId = textIp.text.upper()
            #print(app.classId,textIp.text)
            GlobalShared.classId = app.classId
            print(GlobalShared.classId)
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
            #print(app.subjectId)
            GlobalShared.subjectId = app.subjectId
            print(GlobalShared.subjectId)
        else:
            print("text empty")
    pass
    
    
#attendance code class
class AttendanceDetail(Widget):
    field_AttendanceId = StringProperty(None)
    def setAttendanceId(self):
        try:
            self.field_AttendanceId = "Attendance code: " + str(GlobalShared.attendanceId)
            print(self.field_AttendanceId)
            #app = App.get_running_app()
            #self.attendance_control.ids.anchor_attendance_code.ids.box_attendance_code.ids.attendance_code.text = GlobalShared.attendanceId
            #print(self.attendance_control.ids.anchor_attendance_code.ids.box_attendance_code.ids.attendance_code.text ,GlobalShared.attendanceId)
        except:
            print("error attendance code update")
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
            AttendanceListFromServer = client_teacher.startAttendance(GlobalShared.teacherId, GlobalShared.classId, GlobalShared.subjectId)
            if "error" in AttendanceListFromServer:
                print(AttendanceListFromServer["error"])
            else:
                #save attendance code
                GlobalShared.attendanceId = AttendanceListFromServer["acode"]
                for list in AttendanceListFromServer["student_list"]:
                    #print(list[0], list[1])
                    presence ="Absent"
                    presenceList = [list[1],presence]
                    GlobalShared.attendanceList[list[0]] = presenceList
                print(AttendanceListFromServer["timeout"])
                print(GlobalShared.attendanceList)
        except Exception as e:
            print("error :", e)

class AttendanceControlWindow(Screen):
    attendanceInstance = AttendanceDetail()        
    attendanceInstance.field_AttendanceId = 'No attendance code'
    
    def updateAttendanceSheet(self):
        try:
            AttendanceListFromServer = client_teacher.getAttendance(GlobalShared.teacherId,GlobalShared.classId)
            if "error" in AttendanceListFromServer:
                print(AttendanceListFromServer["error"])
            else:
                print(AttendanceListFromServer["student_list"])
        except Exception as e:
            print(e)

    def finalAttendanceSheet(self):
        try:
            AttendanceListFromServer = client_teacher.stopAttendance(GlobalShared.teacherId,GlobalShared.classId)
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
    def build(self): 
        return kv

if __name__ == "__main__":
    TeacherApp().run()
