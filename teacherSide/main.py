import imp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty
# Window.size = (540, 960)


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
    winH = NumericProperty(Window.size[0])
    winW = NumericProperty(Window.size[1])

    def build(self):
        print(type(self.winH))
        return kv


if __name__ == "__main__":
    TeacherApp().run()
