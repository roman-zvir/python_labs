import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Variables
var_name = tk.StringVar()
var_power_capacity = tk.IntVar()
var_manufacturer = tk.StringVar()
var_price = tk.IntVar()
var_status = tk.StringVar()

# Treeview frame
frame_tree = tk.Frame()
frame_tree.pack()

scrollbar = tk.Scrollbar(frame_tree, orient="vertical")
scrollbar.pack(side="right", fill="y")

tree = ttk.Treeview(
    frame_tree,
    columns=("name", "power capacity", "manufacturer", "price", "status"),
    show="headings",
    selectmode="browse",
    height=10,
    yscrollcommand=scrollbar.set,
)

tree.heading("name", text="Назва", anchor="w")
tree.heading("power capacity", text="Потужність, W", anchor="w")
tree.heading("manufacturer", text="Виробник", anchor="w")
tree.heading("price", text="Ціна", anchor="w")
tree.heading("status", text="Наявність", anchor="w")

tree.column("name", width=150, anchor="w", stretch=True)
tree.column("power capacity", width=120, anchor="w", stretch=False)
tree.column("manufacturer", width=120, anchor="w", stretch=False)
tree.column("price", width=100, anchor="w", stretch=False)
tree.column("status", width=80, anchor="w", stretch=False)

tree.pack()
scrollbar.config(command=tree.yview)

# Sample data
tree.insert("", "end", values=("GameMax", "600", "Ukraine", 2000, True))
tree.insert("", "end", values=("Chieftec", "540", "Poland", 2000, False))
tree.insert("", "end", values=("Panchak Roman", "500", "Ukraine", 1000, True))
tree.insert("", "end", values=("MSI", "900", "Pakistan", 6000, True))
tree.insert("", "end", values=("Gigabyte", "400", "China", 4000, True))
tree.insert("", "end", values=("Cougar 600 pro", "600", "India", 300, False))
tree.insert("", "end", values=("Pccooler", "700", "Germany", 3500, True))
tree.insert("", "end", values=("Deepcool PF-850", "850", "Austria", 7090, True))
tree.insert("", "end", values=("Deepcool PF-750", "750", "Spain", 930, True))
tree.insert("", "end", values=("Seasonik Focus", "1500", "North Korea", 3000, False))
tree.insert("", "end", values=("Corsain BOOM", "480", "Portugal", 3000, True))
tree.insert("", "end", values=("Aerocool Max", "820", "USA", 2000, True))
tree.insert("", "end", values=("ASUS SUS", "700", "Canada", 1000, True))
tree.insert("", "end", values=("RZTK power", "940", "Mexico", 6000, True))
tree.insert("", "end", values=("Zalmar top", "2000", "China", 4000, True))
tree.insert("", "end", values=("Electron", "800", "Ukraine", 300, True))
tree.insert("", "end", values=("Nordic", "600", "Sweden", 3500, True))
tree.insert("", "end", values=("911", "911", "Afghanistan", 7040, True))
tree.insert("", "end", values=("Francisco", "700", "Vatican city", 9030, True))
tree.insert("", "end", values=("Aigo", "400", "Estonia", 2500, False))

tree.selection_set(tree.get_children()[0])

# Frame for entry fields
labelframe_entry = tk.LabelFrame(root, text="Enter Data")
labelframe_entry.pack(padx=10, pady=10)

# Name entry
label_name = tk.Label(labelframe_entry, text="Name:")
label_name.pack()
entry_name = tk.Entry(labelframe_entry, textvariable=var_name)
entry_name.pack()

# Power capacity entry
label_power_capacity = tk.Label(labelframe_entry, text="Power Capacity (W):")
label_power_capacity.pack()
entry_power_capacity = tk.Entry(labelframe_entry, textvariable=var_power_capacity)
entry_power_capacity.pack()

# Manufacturer entry
label_manufacturer = tk.Label(labelframe_entry, text="Manufacturer:")
label_manufacturer.pack()
entry_manufacturer = tk.Entry(labelframe_entry, textvariable=var_manufacturer)
entry_manufacturer.pack()

# Price scale
scale_price = tk.Scale(
    labelframe_entry,
    variable=var_price,
    from_=1000,
    to=10000,
    tickinterval=9000,
    resolution=100,
    orient="horizontal",
)
scale_price.pack()

# Status combobox
combo_status = ttk.Combobox(
    labelframe_entry,
    textvariable=var_status,
    values=("True", "False", "No Data"),
)
combo_status.pack()

# Reset variables
var_name.set("")
var_price.set(0)
var_status.set("False")

# Frame for buttons
labelframe_button = tk.LabelFrame(root)
labelframe_button.pack(padx=10, pady=10)


# Insert button
def handle_insert():
    name = var_name.get()
    power_capacity = var_power_capacity.get()
    manufacturer = var_manufacturer.get()
    price = var_price.get()
    status = var_status.get()

    if name == "" or manufacturer == "" or power_capacity == 0:
        return

    tree.insert("", "end", values=(name, power_capacity, manufacturer, price, status))
    var_name.set("")
    var_manufacturer.set("")
    var_power_capacity.set(0)
    var_price.set(0)
    var_status.set("False")


button_insert = tk.Button(
    labelframe_button,
    text="Insert",
    command=handle_insert,
)
button_insert.grid(row=0, column=0, padx=5)


# Delete button
def handle_delete():
    selection = tree.selection()
    if not selection:
        return
    tree.delete(selection[0])


button_delete = tk.Button(
    labelframe_button,
    text="Delete",
    command=handle_delete,
)
button_delete.grid(row=0, column=1, padx=5)


# Get item button
def handle_get_item():
    selection = tree.selection()
    if not selection:
        return
    values = tree.item(selection[0]).get("values")
    var_name.set(values[0])
    var_manufacturer.set(values[2])
    var_power_capacity.set(values[1])
    var_price.set(values[3])
    var_status.set(values[4])


button_get = tk.Button(
    labelframe_button,
    text="Get",
    command=handle_get_item,
)
button_get.grid(row=0, column=2, padx=5)


# Set button
def handle_set():
    selection = tree.selection()
    name = var_name.get()
    power_capacity = var_power_capacity.get()
    manufacturer = var_manufacturer.get()
    price = var_price.get()
    status = var_status.get()

    if name == "" or not selection:
        return

    tree.set(selection[0], column="name", value=name)
    tree.set(selection[0], column="power capacity", value=power_capacity)
    tree.set(selection[0], column="manufacturer", value=manufacturer)
    tree.set(selection[0], column="price", value=price)
    tree.set(selection[0], column="status", value=status)

    var_name.set("")
    var_manufacturer.set("")
    var_power_capacity.set(0)
    var_price.set(0)
    var_status.set("False")


button_set = tk.Button(
    labelframe_button,
    text="Set",
    command=handle_set,
)
button_set.grid(row=0, column=3, padx=5)

root.mainloop()
