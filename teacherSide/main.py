import imp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.dropdown import DropDown
# Window.size = (540, 960)


class MainWindow(Screen):

    prevColor = [1, 1, 1, 1]

    # textTest = ObjectProperty(None)
    def buttonPressed(self, btn, recentUsedColor):
        self.prevColor = btn.background_color
        btn.background_color = recentUsedColor

    def exitingButtonPress(self, btn):
        btn.background_color = self.prevColor
    pass


class BctCDWindow(Screen):
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
