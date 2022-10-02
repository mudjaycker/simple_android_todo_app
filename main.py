from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime as dt
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
# from kivy.core.window import Window
from kivy.utils import platform

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

from db import DB

db = DB()

# Window.size = (350, 600)

class ListItemWithCheckBox(TwoLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    
    def mark(self, check, the_list_item):
        if check.active == True:
            the_list_item.text = f"[s]{the_list_item.text}[/s]"
            db.mark_task_as_complete(the_list_item.pk)
        else:
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))

    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)


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

    def on_start(self):
        try:
            completed_tasks, uncomplete_tasks = db.get_tasks()
            if uncomplete_tasks != []:
                for task in uncomplete_tasks:
                    add_task = ListItemWithCheckBox(pk=task[0], text=task[1], secondary_text=task[2])
                    self.root.ids.container.add_widget(add_task)

            if completed_tasks != []:
                for task in completed_tasks:
                    add_task = ListItemWithCheckBox(pk=task[0], text=f"[s]{task[1]}[/s]", secondary_text=task[2])
                    add_task.ids.check.active = True
                    self.root.ids.container.add_widget(add_task)
        except Exception as e:
            print(e)
            pass
        return super().on_start()

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
        # print(task.text, task_date)
        created_task = db.create_task(task.text, task_date)
        self.root.ids['container'].add_widget(ListItemWithCheckBox(pk=created_task[0],text=f"[b]{created_task[1]}[/b]", secondary_text=created_task[2]))
        task.text = ""
    







if __name__ == "__main__":
    app = MainApp()
    app.run()