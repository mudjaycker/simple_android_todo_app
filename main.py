from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime as dt
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.core.window import Window

Window.size = (350, 600)

class ListItemWithCheckBox(TwoLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    
    def mark(self, check, the_list_item):
        if check.active == True:
            the_list_item.text = f"[s]{the_list_item.text}[/s]"
        else:
            pass

    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom left container'''

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
        self.theme_cls.primary_palette = "LightGreen"


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
        self.root.ids['container'].add_widget(ListItemWithCheckBox(text=f"[b]{task.text}[/b]", secondary_text=task_date))
        task.text = ""

if __name__ == "__main__":
    app = MainApp()
    app.run()