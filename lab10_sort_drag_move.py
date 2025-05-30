import tkinter as tk
from tkinter import ttk
import locale

people = [
    ("Петерега", "ПП", 100),
    ("Шевченко", "ПЗ", 5),
    ("Гнатюк", "ОІ", 6),
    ("Мельничук", "УП", 5),
    ("Романенко", "ШІ", 20),
    ("Остапчук", "КН", 6),
    ("Литвин", "КІ", 2),
    ("Іванишин", "КБ", 34),
    ("Тимошенко", "ФЛ", 12),
    ("Деркач", "КНІТ", 30),
    ("Петренко", "ПП", 10),
    ("Сидоренко", "ПЗ", 15),
    ("Коваленко", "ОІ", 8),
    ("Ткаченко", "УП", 20),
    ("Грищенко", "ШІ", 25),
    ("Мороз", "КН", 18),
    ("Бондаренко", "КІ", 22),
    ("Кравченко", "КБ", 14),
    ("Левченко", "ФЛ", 16),
    ("Дорошенко", "КНІТ", 28),
    ("Савченко", "ПП", 12),
    ("Костенко", "ПЗ", 9),
    ("Шаповал", "ОІ", 11),
    ("Гончар", "УП", 13),
    ("Костюк", "ШІ", 17),
    ("Бондар", "КН", 19),
    ("Тимчук", "КІ", 21),
    ("Федоренко", "КБ", 23),
    ("Мельник", "ФЛ", 24),
    ("Семененко", "КНІТ", 26),
]

root = tk.Tk()
root.title("Співробітники кафедр")
root.geometry("620x400")
root.configure(bg="#f5f5f5")

# Apply a modern theme if available
try:
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "light")
except tk.TclError:
    style = ttk.Style()
    style.theme_use("clam")

# Configure styles
style = ttk.Style()
style.configure(
    "Treeview",
    background="#f9f9f9",
    foreground="black",
    rowheight=25,
    fieldbackground="#f9f9f9",
)
style.configure(
    "Treeview.Heading",
    font=("Helvetica", 10, "bold"),
    background="#e0e0e0",
    foreground="black",
)
style.map("Treeview", background=[("selected", "#0078d7")])

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

title_label = ttk.Label(
    main_frame, text="Список співробітників", font=("Helvetica", 14, "bold")
)
title_label.pack(pady=(0, 10))

order = {"name": False, "department": False, "experience": False}
locale.setlocale(locale.LC_COLLATE, "uk_UA.UTF-8")


def update_row_tags():
    for index, iid in enumerate(treeview.get_children()):
        tag = "oddrow" if index % 2 == 0 else "evenrow"
        treeview.item(iid, tags=(tag,))


def handle_sort(column):
    children = treeview.get_children()
    if column == "experience":
        rows = [(int(treeview.set(iid, column)), iid) for iid in children]
    else:
        rows = [(locale.strxfrm(treeview.set(iid, column)), iid) for iid in children]
    rows.sort(key=lambda t: t[0], reverse=order[column])
    for index, (_, iid) in enumerate(rows):
        treeview.move(iid, "", index)
    arrow = "\u25bc" if order[column] else "\u25b2"
    text_name = f"Прізвище {arrow}" if column == "name" else "Прізвище"
    text_department = f"Кафедра {arrow}" if column == "department" else "Кафедра"
    text_experience = f"Стаж {arrow}" if column == "experience" else "Стаж"
    treeview.heading("name", text=text_name, command=lambda: handle_sort("name"))
    treeview.heading(
        "department", text=text_department, command=lambda: handle_sort("department")
    )
    treeview.heading(
        "experience", text=text_experience, command=lambda: handle_sort("experience")
    )
    order[column] = not order[column]
    update_row_tags()


tree_frame = ttk.Frame(main_frame)
tree_frame.pack(fill="both", expand=True)

scrollbar = ttk.Scrollbar(tree_frame)
scrollbar.pack(side="right", fill="y")

treeview = ttk.Treeview(
    tree_frame,
    columns=("name", "department", "experience"),
    show="headings",
    yscrollcommand=scrollbar.set,
)
treeview.pack(fill="both", expand=True)
scrollbar.config(command=treeview.yview)

treeview.heading("name", text="Прізвище", command=lambda: handle_sort("name"))
treeview.heading(
    "department", text="Кафедра", command=lambda: handle_sort("department")
)
treeview.heading("experience", text="Стаж", command=lambda: handle_sort("experience"))

treeview.column("name", anchor="w", width=200)
treeview.column("department", anchor="center", width=150)
treeview.column("experience", anchor="center", width=100)

treeview.tag_configure("oddrow", background="#f0f8ff")
treeview.tag_configure("evenrow", background="#ffffff")

for index, person in enumerate(people):
    tag = "oddrow" if index % 2 == 0 else "evenrow"
    treeview.insert("", "end", values=person, tags=(tag,))

dragging_item = None


def on_button_press(e):
    global dragging_item
    item = treeview.identify_row(e.y)
    if not item:
        return
    dragging_item = item
    treeview.selection_set(dragging_item)
    treeview.focus(dragging_item)


def on_mouse_drag(e):
    global dragging_item
    if not dragging_item:
        return
    target_item = treeview.identify_row(e.y)
    if not target_item or dragging_item == target_item:
        return
    index = treeview.index(target_item)
    treeview.move(dragging_item, "", index)


def on_button_release(e):
    global dragging_item
    dragging_item = None
    update_row_tags()


# ...existing code...


def on_key_move(move):
    selected = treeview.selection()
    if not selected:
        return
    selected_item = selected[0]
    index = treeview.index(selected_item)
    new_index = index - 1 if move == "up" else index + 1
    if 0 <= new_index < len(treeview.get_children()):
        treeview.move(selected_item, "", new_index)
        treeview.selection_set(selected_item)
        treeview.focus(selected_item)
        update_row_tags()


def on_key_move_extreme(move):
    selected = treeview.selection()
    if not selected:
        return
    selected_item = selected[0]
    new_index = 0 if move == "top" else len(treeview.get_children()) - 1
    treeview.move(selected_item, "", new_index)
    treeview.selection_set(selected_item)
    treeview.focus(selected_item)
    update_row_tags()


treeview.bind("<ButtonPress-1>", on_button_press)
treeview.bind("<B1-Motion>", on_mouse_drag)
treeview.bind("<ButtonRelease-1>", on_button_release)

treeview.bind("<KeyPress-Page_Up>", lambda e: on_key_move("up"))
treeview.bind("<KeyPress-Page_Down>", lambda e: on_key_move("down"))
treeview.bind("<KeyPress-Home>", lambda e: on_key_move_extreme("top"))
treeview.bind("<KeyPress-End>", lambda e: on_key_move_extreme("bottom"))

status_frame = ttk.Frame(main_frame)
status_frame.pack(fill="x", pady=(10, 0))
status_label = ttk.Label(
    status_frame,
    text="Підказка: Використовуйте клавіші Page Up/Down для зміни порядку, "
    "Home/End для переміщення в початок/кінець",
)
status_label.pack(side="left")
root.mainloop()
