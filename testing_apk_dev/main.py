from kivy.app import App
from kivy.uix.widget import Widget

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label


class TeacherApp(App):
    def build(self):
    
        self.img1 = Image(source="assets/logo.png",size_hint=(1, .8))
        self.verificationLabel = Label(
            text="Your solution to attendance", size_hint=(1, .1))
        self.btn1 = Button(text='Start Atteandance', size_hint=(1, .1))

    	# layout of app
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.img1)
        layout.add_widget(self.verificationLabel)
        layout.add_widget(self.btn1)
        
        return layout

TeacherApp().run()

