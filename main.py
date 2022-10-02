from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime
from kivy.core.window import Window

Window.size = (300, 600)


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"



if __name__ == "__main__":
    app = MainApp()
    app.run()