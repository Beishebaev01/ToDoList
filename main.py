import flet as ft
from db import main_db
import datetime as dt


def main(page: ft.Page):
    page.title = "To-Do List"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_maximized = True

    task_list = ft.Column(spacing=10)

    filter_type = "all"


    def add_date_to_task(task_text):
        return f"{task_text} [{dt.datetime.now().strftime('%d.%m %H:%M')}]"


    def load_task():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks_db(filter_type):
            task_list.controls.append(create_task_row(task_id, task_text, completed))
        page.update()


    def create_task_row(task_id, task_text, completed):
        task_field = ft.TextField(value=task_text, expand=True, dense=True, read_only=True)
        task_checkbox = ft.Checkbox(value=bool(completed), on_change=lambda e: toggle_task(task_id, e.control.value))

        def enable_edit(_):
            task_field.read_only = False
            page.update()

        def save_edit(_):
            new_text = task_field.value.split(' [')[0]

            if len(new_text) > 2:
                page.snack_bar = ft.SnackBar(ft.Text("Задача не может быть длиннее 100 символов!"), open=True)
                return

            updated_text = add_date_to_task(new_text)
            main_db.update_task_db(task_id, task_field.value)
            task_field.read_only = True
            task_field.value = updated_text
            page.update()
        
        return ft.Row([
            task_checkbox,
            task_field,
            ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(ft.icons.SAVE, icon_color=ft.colors.GREEN_400, on_click=save_edit),
            ft.IconButton(ft.icons.DELETE, icon_color=ft.colors.RED_400, on_click=lambda _: delete_task(task_id))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    
    def add_task(_):
        task_text = task_input.value.strip()
        if not task_text:
            return
            
        if len(task_text) > 2:
            page.snack_bar = ft.SnackBar(ft.Text("Задача не может быть длиннее 100 символов!"))
            page.snack_bar.open = True
            page.update()
            return
            
        task_with_date = add_date_to_task(task_text)
        task_id = main_db.add_task_db(task_with_date)
        task_list.controls.append(create_task_row(task_id, task_with_date, completed=0))
        task_input.value = ""
        page.update()


    def toggle_task(task_id, is_completed):
        main_db.update_task_db(task_id, completed=int(is_completed))
        load_task()

    def delete_task(task_id):
        main_db.delete_task_db(task_id)
        load_task()

    def set_filter(filter_value):
        nonlocal filter_type

        filter_type = filter_value
        load_task()

    
    task_input = ft.TextField(hint_text="Add task", dense=True, expand=True, on_submit=add_task, max_length=3)
    add_button = ft.ElevatedButton("Add", on_click=add_task, icon=ft.icons.ADD)
    filter_button = ft.Row([
        ft.ElevatedButton("All", on_click=lambda e: set_filter("all")),
        ft.ElevatedButton("Completed", on_click=lambda e: set_filter("completed")),
        ft.ElevatedButton("Incompleted", on_click=lambda e: set_filter("incompleted"))                  
    ], alignment=ft.MainAxisAlignment.CENTER)


    content = ft.Container(
        content=ft.Column([
            ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            filter_button,
            task_list
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        alignment=ft.alignment.center
    )

    background_image = ft.Image(
        src="/home/bshv01/Desktop/ToDoList/image.png",
        fit=ft.ImageFit.FILL,
        width=page.width,
        height=page.height
    )

    background = ft.Stack([
        background_image,
        content
    ])

    def on_resize(_):
        background_image.width = page.width
        background_image.height = page.height
        page.update()


    page.add(background)
    page.on_resized = on_resize


    load_task()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)