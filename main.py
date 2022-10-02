from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime as dt
from kivy.core.window import Window

Window.size = (350, 600)

class DialogContent(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.date_text.text = str(dt.now().strftime("%A %d %B %Y"))
    

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()


    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y")
        self.ids.date_text.text = str(date)  





class MainApp(MDApp):
    task_list_dialog = None
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"


    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title ="Create Task",
                type = "custom",
                content_cls = DialogContent()
            )
        self.task_list_dialog.open()
    
    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()
    
    def add_task(self, task, task_date):
        print(task.text, task_date)
        task.text = ""

if __name__ == "__main__":
    app = MainApp()
    app.run()