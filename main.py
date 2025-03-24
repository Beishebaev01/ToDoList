import flet as ft
from db import main_db
import datetime as dt


def main(page: ft.Page):
    page.title = "To-Do List"
    page.padding = 75
    page.bgcolor= ft.colors.GREY_800
    page.theme_mode = ft.ThemeMode.SYSTEM

    task_list = ft.Column(spacing=10)


    def add_date_to_task(task_text):
        return f"{task_text} [{dt.datetime.now().strftime('%d.%m %H:%M')}]"


    def load_task():
        task_list.controls.clear()
        for task_id, task_text in main_db.get_tasks_db():
            task_list.controls.append(create_task_row(task_id, task_text))
        page.update()


    def create_task_row(task_id, task_text):
        task_field = ft.TextField(value=task_text, expand=True, dense=True, read_only=True)

        def enable_edit(_):
            task_field.read_only = False
            page.update()

        def save_edit(_):
            new_text = task_field.value.split(' [')[0]
            updated_text = add_date_to_task(new_text)
            main_db.update_task_db(task_id, task_field.value)
            task_field.read_only = True
            task_field.value = updated_text
            page.update()
        
        return ft.Row([
            task_field,
            ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(ft.icons.SAVE, icon_color=ft.colors.GREEN_400, on_click=save_edit)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    
    def add_task(_):
        if task_input.value.strip():
            task_with_date = add_date_to_task(task_input.value)
            task_id = main_db.add_task_db(task_with_date)
            task_list.controls.append(create_task_row(task_id, task_with_date))
            task_input.value = ""
            page.update()

    
    task_input = ft.TextField(hint_text="Add task", dense=True, expand=True, on_submit=add_task)
    add_button = ft.ElevatedButton("Add", on_click=add_task, icon=ft.icons.ADD)

    page.add(
        ft.Column([
            ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                task_list
                ])
    )

    load_task()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)