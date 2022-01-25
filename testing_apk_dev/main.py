from kivy.app import App
from kivy.uix.widget import Widget

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2
import numpy as np
import face_recognition

imag = face_recognition.load_image_file("assets/pic.jpg")
imag = cv2.cvtColor(imag, cv2.COLOR_BGR2RGB)
encodingsTest = face_recognition.face_encodings(imag)[0]


class CamApp(App):

    def build(self):
        # opencv2 stuffs
        self.img1 = Image(size_hint=(1, .8))
        self.verificationLabel = Label(
            text="Verification Uninitiated", size_hint=(1, .1))
        self.btn1 = Button(text='Verify', size_hint=(1, .1))

        # layout of app
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.img1)
        layout.add_widget(self.verificationLabel)
        layout.add_widget(self.btn1)

        # Setup video capture device
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/33.0)

        return layout

    def update(self, dt):

        # display image from cam in opencv window
        success, frame = self.capture.read()

        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')

        # if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer.
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        # display image from the texture
        self.img1.texture = texture1
        # self.faceRecog()

if __name__ == '__main__':
    CamApp().run()
    cv2.destroyAllWindows()
