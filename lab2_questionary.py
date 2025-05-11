import tkinter as tk

root = tk.Tk()

# Entry ---------------------------------------------------------------
entry_var = tk.StringVar()
entry = tk.Entry(
    bg="white",
    textvariable=entry_var
)
entry.pack()

# Radiobutton --------------------------------------------------------
radiobutton_var = tk.StringVar()
radiobutton_frame = tk.LabelFrame(
    root,
    text="Radiobutton",
    bd=1,
    relief="solid",
)
radiobutton_frame.pack()

radiobutton0 = tk.Radiobutton(
    radiobutton_frame,
    variable=radiobutton_var,
    value="Nano",
    text="Nano",
)
radiobutton0.pack()

radiobutton1 = tk.Radiobutton(
    radiobutton_frame,
    variable=radiobutton_var,
    value="Micro",
    text="Micro",
)
radiobutton1.pack()

radiobutton2 = tk.Radiobutton(
    radiobutton_frame,
    variable=radiobutton_var,
    value="Milli",
    text="Milli",
)
radiobutton2.pack()

# Checkbutton --------------------------------------------------------
checkbutton_var0 = tk.BooleanVar()
checkbutton_var1 = tk.BooleanVar()
checkbutton_var2 = tk.BooleanVar()

checkbutton_frame = tk.LabelFrame(
    root,
    text="Checkbutton",
    bd=1,
    relief="solid",
)
checkbutton_frame.pack()

checkbutton0 = tk.Checkbutton(
    checkbutton_frame,
    variable=checkbutton_var0,
    onvalue=True,
    offvalue=False,
    text="Nano",
)
checkbutton0.pack()

checkbutton1 = tk.Checkbutton(
    checkbutton_frame,
    variable=checkbutton_var1,
    onvalue=True,
    offvalue=False,
    text="Micro",
)
checkbutton1.pack()

checkbutton2 = tk.Checkbutton(
    checkbutton_frame,
    variable=checkbutton_var2,
    onvalue=True,
    offvalue=False,
    text="Milli",
)
checkbutton2.pack()

# Spinbox -------------------------------------------------------------
spinbox_var = tk.StringVar()
spinbox = tk.Spinbox(
    textvariable=spinbox_var,
    values=("Nano", "Micro", "Milli"),
    state="readonly",
)
spinbox.pack()

# OptionMenu ----------------------------------------------------------
optionmenu_var = tk.StringVar()
optionmenu = tk.OptionMenu(
    root,
    optionmenu_var,
    "Nano", "Micro", "Milli",
)
optionmenu.pack()

# Label -------------------------------------------------------------
label = tk.Label(bg="white")
label.pack()

# Function to get values ---------------------------------------------
def get_values():
    nano_cntr, micro_cntr, milli_cntr = 0, 0, 0

    # Check entry value
    nano_cntr += 1 if entry_var.get() == "Nano" else 0
    micro_cntr += 1 if entry_var.get() == "Micro" else 0
    milli_cntr += 1 if entry_var.get() == "Milli" else 0

    # Check radiobutton value
    if radiobutton_var.get() == "Nano":
        nano_cntr += 1
    elif radiobutton_var.get() == "Micro":
        micro_cntr += 1
    elif radiobutton_var.get() == "Milli":
        milli_cntr += 1

    # Check checkbutton values
    nano_cntr += 1 if checkbutton_var0.get() else 0
    micro_cntr += 1 if checkbutton_var1.get() else 0
    milli_cntr += 1 if checkbutton_var2.get() else 0

    # Check spinbox value
    if spinbox_var.get() == "Nano":
        nano_cntr += 1
    elif spinbox_var.get() == "Micro":
        micro_cntr += 1
    elif spinbox_var.get() == "Milli":
        milli_cntr += 1

    # Check OptionMenu value
    if optionmenu_var.get() == "Nano":
        nano_cntr += 1
    elif optionmenu_var.get() == "Micro":
        micro_cntr += 1
    elif optionmenu_var.get() == "Milli":
        milli_cntr += 1

    # Update label with counts
    label.config(text=f"Nano={nano_cntr}, Micro={micro_cntr}, Milli={milli_cntr}")

# Button -------------------------------------------------------------
button = tk.Button(
    text="Get Values",
    command=get_values,
)
button.pack()

# Main loop ----------------------------------------------------------
root.mainloop()