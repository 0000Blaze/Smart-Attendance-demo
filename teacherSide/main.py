from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

class MainWindow(Screen):
    pass


class BctWindow(Screen):
    pass

class BexWindow(Screen):
    pass

class BelWindow(Screen):
    pass

class SectionWindow(Screen):
    pass

class BctCDWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class TeacherApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    TeacherApp().run()