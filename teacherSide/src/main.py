#!/usr/bin/env python
import GlobalShared
import utility
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
            GlobalShared.teacherId = app.teacherId
            print(GlobalShared.teacherId)
        else:
            print("text empty")
    pass
    def setClassId(self, app, textIp):
        if textIp != "":
            app.classId = textIp.text.upper()
            GlobalShared.classId = app.classId
            print(GlobalShared.classId)
        else:
            print("text empty")
    pass

#subject id selection class
class SubjectSelect(Widget):
    field_id = ObjectProperty(None)
    field_subject = StringProperty(None)

    def setSubjectCode(self):
        try:
            self.field_subject = GlobalShared.subjectname
            if len(GlobalShared.subjectname)>20:
                self.field_subject = GlobalShared.subjectname[:18]+"..."
            print(self.field_subject)
        except:
            print("error setting scode")
    pass
    
    
#attendance code class
class AttendanceDetail(Widget):
    field_AttendanceId = StringProperty(None)

    def setAttendanceId(self):
        try:
            self.field_AttendanceId = "Attendance code: " + str(GlobalShared.attendanceId)
            print(self.field_AttendanceId)
        except:
            print("error attendance code update")
    pass

    def clearAttendanceCode(self):
        GlobalShared.attendanceId = ""
        self.field_AttendanceId = "No attendance code"

''' ############################################### Classes for kivy windows ############################################### '''
class MainWindow(Screen):
    stdTid = TeacherIdInput()
    stdTid.field_id = ObjectProperty(None)
    stdTid.field_text = 'Teacher Id:'
    stdTid.field_placeholder = 'Example : 011'

    stdClass = TeacherIdInput()
    stdClass.field_id = ObjectProperty(None)
    stdClass.field_text = 'Class Id:'
    stdClass.field_placeholder = 'Example : PUL075BCTCD'

    prevColor = [1, 1, 1, 1]
    def buttonPressed(self, btn, recentUsedColor):
        self.prevColor = btn.background_color
        btn.background_color = recentUsedColor
    pass
    def exitingButtonPress(self, btn):
        btn.background_color = self.prevColor
    pass 
    
    def getSubjectList(self):
        try:
            subjectListFromServer = client_teacher.updateClassAndSubjects(GlobalShared.teacherId)
            GlobalShared.subjectId = subjectListFromServer["subject"][0][0]
            GlobalShared.subjectname = subjectListFromServer["subject"][0][1]
            print(GlobalShared.subjectId)
        except:
            print("Subject retrival error")
                

class SubjectSelectWindow(Screen):
    stdSid = SubjectSelect()
    stdSid.field_id = ObjectProperty(None)
    stdSid.field_subject = 'Subject Id:'
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

        except Exception as e:
            print("error :", e)

class AttendanceControlWindow(Screen):
    attendanceInstance = AttendanceDetail()        
    attendanceInstance.field_AttendanceId = 'No attendance code'
        
    def addPresentList(self):
        x = 0
        y = 0
        z = 0
        for name in utility.convertdictToList(GlobalShared.attendanceList):
            self.ids.rv.add_widget(
                Label(text=name, pos=(130+z, 350+y), font_size=12))
            x = x+1
            y = y-15
            if x == 24:
                z = 400
                y = 0
    
    def removePresentList(self):
        for name in utility.convertdictToList(GlobalShared.attendanceList):
            self.ids.rv.clear_widgets()

    def updateAttendanceSheet(self):
        try:
            AttendanceListFromServer = client_teacher.getAttendance(GlobalShared.teacherId,GlobalShared.classId)
            if "error" in AttendanceListFromServer:
                print(AttendanceListFromServer["error"])
            else:
                #update presence in list
                keys = AttendanceListFromServer["student_list"]
                for key in keys:
                    GlobalShared.attendanceList[key][1] = "Present"
                    self.removePresentList()
                #display attendance list
                self.addPresentList()
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

    def manualPresent(self,text):
        try:
            text.text =str(text.text)
            text.text.upper()
            if (text.text != ""):
                client_teacher.markAttendance(GlobalShared.teacherId,GlobalShared.classId,text.text)
            text.text = ""
        except:
            print("some error occured during manual attendance")

''' ############################################### Kivy App builder ################################################ '''
class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class TeacherApp(App):    
    def build(self): 
        return kv

if __name__ == "__main__":
    TeacherApp().run()
