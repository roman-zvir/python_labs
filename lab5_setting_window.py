import tkinter as tk
import tkinter.ttk as ttk
from tkinter import colorchooser

top_level = None
root = tk.Tk()

# Variables
text_var = tk.StringVar()
family_var = tk.StringVar()
size_var = tk.IntVar()
weight_var = tk.StringVar()
bg_var = tk.StringVar()
fg_var = tk.StringVar()

# Root window settings
root.geometry("200x200")
root.resizable(False, False)

# Handlers
def handle_close():
    global top_level
    top_level.grab_release()
    top_level.destroy()
    top_level = None

def handle_ok():
    label.config(
        text=text_var.get(),
        font=(family_var.get(), int(size_var.get()), weight_var.get()),
        bg=bg_var.get(),
        fg=fg_var.get(),
    )
    handle_close()

def handle_cancel():
    handle_close()

def handle_adjust():
    global top_level
    if top_level is not None:
        return

    top_level = tk.Toplevel(root)
    top_level.title("Adjust")
    top_level.resizable(False, False)
    top_level.protocol("WM_DELETE_WINDOW", handle_close)
    top_level.geometry("450x450")

    # Extract current font properties
    family, size, weight = label.cget("font").split(" ")

    # Text frame
    frame_text = tk.LabelFrame(top_level, text="Text:")
    frame_text.pack(fill="x", padx=5, pady=5)
    entry_text = tk.Entry(frame_text, textvariable=text_var)
    entry_text.pack(fill="x", padx=5, pady=5)
    text_var.set(label.cget("text"))

    # Font family frame
    frame_family = tk.LabelFrame(top_level, text="Font Family:")
    frame_family.pack(fill="x", padx=5, pady=5)
    combo_family = ttk.Combobox(
        frame_family,
        textvariable=family_var,
        values=("Arial", "Times", "Verdana"),
        width=15,
        state="readonly",
    )
    combo_family.pack(padx=5, pady=5)
    family_var.set(family)

    # Font size frame
    frame_size = tk.LabelFrame(top_level, text="Font Size:")
    frame_size.pack(fill="x", padx=5, pady=5)
    spin_size = tk.Spinbox(
        frame_size,
        textvariable=size_var,
        values=("8", "9", "10", "11", "12", "13", "14", "15"),
        width=15,
        state="readonly",
    )
    spin_size.pack(padx=5, pady=5)
    size_var.set(int(size))

    # Font weight frame
    frame_weight = tk.LabelFrame(top_level, text="Font Weight:")
    frame_weight.pack(fill="x", padx=5, pady=5)
    combo_weight = ttk.Combobox(
        frame_weight,
        textvariable=weight_var,
        values=("normal", "bold"),
        width=15,
        state="readonly",
    )
    combo_weight.pack(padx=5, pady=5)
    weight_var.set(weight)

    # Colors frame
    frame_colors = tk.LabelFrame(top_level, text="Colors:")
    frame_colors.pack(fill="x", padx=5, pady=5)

    # Background color
    frame_bg = tk.Frame(frame_colors)
    frame_bg.pack(fill="x", padx=5, pady=2)
    tk.Label(frame_bg, text="Background:").pack(side="left")
    entry_bg = tk.Entry(frame_bg, textvariable=bg_var, width=8)
    entry_bg.pack(side="left", padx=5)
    bg_var.set(label.cget("bg"))

    def choose_bg_color():
        color = colorchooser.askcolor(initialcolor=bg_var.get())[1]
        if color:
            bg_var.set(color)

    tk.Button(frame_bg, text="Choose...", command=choose_bg_color).pack(side="right")

    # Foreground color
    frame_fg = tk.Frame(frame_colors)
    frame_fg.pack(fill="x", padx=5, pady=2)
    tk.Label(frame_fg, text="Foreground:").pack(side="left")
    entry_fg = tk.Entry(frame_fg, textvariable=fg_var, width=8)
    entry_fg.pack(side="left", padx=5)
    fg_var.set(label.cget("fg") if label.cget("fg") else "black")

    def choose_fg_color():
        color = colorchooser.askcolor(initialcolor=fg_var.get())[1]
        if color:
            fg_var.set(color)

    tk.Button(frame_fg, text="Choose...", command=choose_fg_color).pack(side="right")

    # Buttons
    button_ok = tk.Button(top_level, text="Ok", width=15, command=handle_ok)
    button_ok.pack(side="left", padx=5, pady=5, expand=True)

    button_cancel = tk.Button(top_level, text="Cancel", width=15, command=handle_cancel)
    button_cancel.pack(side="right", padx=5, pady=5, expand=True)

    top_level.grab_set()

# Default handler
def handle_default():
    # Reset label to default settings
    label.config(
        bg="white",
        text="Enter text...",
        font=("Arial", 10, "normal"),
        anchor="center",
        width=20,
        height=3,
        fg="black",
    )

# Initialize label with all properties
label = tk.Label(
    bg="white",
    text="Enter text...",
    font=("Arial", 10, "normal"),
    anchor="center",
    width=20,
    height=3,
    fg="black",
)
label.pack(padx=10, pady=10)

# Buttons
button_adjust = tk.Button(text="Adjust", width=10, command=handle_adjust)
button_adjust.pack(pady=5)

button_default = tk.Button(text="Default", width=10, command=handle_default)
button_default.pack(pady=5)

# Main loop
root.mainloop()