from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
Window.size = (540, 960)


class RollNoInput(Widget):
    field_id = ObjectProperty(None)
    field_text = StringProperty(None)
    field_placeholder = StringProperty(None)
    text = ""

    def getText(self):
        return self.field_text

    def getPlaceHolder(self):
        return self.field_placeholder

    def process(self, txt):
        if txt.text != "":
            self.text = txt.text
            print(self.text)
        else:
            print("text empty")
    pass


class MainWindow(Screen):
    stdRoll = RollNoInput()
    stdRoll.field_id = ObjectProperty(None)
    stdRoll.field_text = 'Roll No:'
    stdRoll.field_placeholder = 'Enter Roll no:'
    stdRoll.text = ""
    pass


class CameraWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("student.kv")


class StudentApp(App):

    def build(self):
        return kv


if __name__ == "__main__":
    StudentApp().run()
