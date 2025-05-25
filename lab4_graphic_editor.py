import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Line Editor")
root.minsize(1000, 500)  # Set minimum window size

# Create main frames with proper weights
control_frame = tk.Frame(root, padx=10, pady=10)
control_frame.grid(row=0, column=0, sticky="nw")

canvas_frame = tk.LabelFrame(
    root, text="Canvas area", bd=2, relief="groove", padx=5, pady=5
)
canvas_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Configure grid weights for resizing
root.grid_columnconfigure(1, weight=1)  # Canvas column expands
root.grid_rowconfigure(0, weight=1)  # Row expands

# Create canvas with proper expansion
canvas = tk.Canvas(canvas_frame, bg="white", width=400, height=400)
canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Variables
dash_var = tk.StringVar()
x1_var = tk.IntVar()
y1_var = tk.IntVar()
x2_var = tk.IntVar()
y2_var = tk.IntVar()
width_var = tk.IntVar()
fill_var = tk.StringVar()

# First point frame
frame_x1_y1 = tk.LabelFrame(
    control_frame, text="First point:", bd=2, relief="groove", padx=5, pady=5
)
frame_x1_y1.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

frame_x1 = tk.LabelFrame(frame_x1_y1, text="x:", bd=1, relief="solid")
frame_x1.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
spinbox_x1 = tk.Spinbox(frame_x1, textvariable=x1_var, from_=0, to=500, width=5)
spinbox_x1.grid(row=0, column=0, padx=5, pady=5)

frame_y1 = tk.LabelFrame(frame_x1_y1, text="y:", bd=1, relief="solid")
frame_y1.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
spinbox_y1 = tk.Spinbox(frame_y1, textvariable=y1_var, from_=0, to=500, width=5)
spinbox_y1.grid(row=0, column=0, padx=5, pady=5)

# Second point frame
frame_x2_y2 = tk.LabelFrame(
    control_frame, text="Second point:", bd=2, relief="groove", padx=5, pady=5
)
frame_x2_y2.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

frame_x2 = tk.LabelFrame(frame_x2_y2, text="x:", bd=1, relief="solid")
frame_x2.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
spinbox_x2 = tk.Spinbox(frame_x2, textvariable=x2_var, from_=0, to=500, width=5)
spinbox_x2.grid(row=0, column=0, padx=5, pady=5)

frame_y2 = tk.LabelFrame(frame_x2_y2, text="y:", bd=1, relief="solid")
frame_y2.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
spinbox_y2 = tk.Spinbox(frame_y2, textvariable=y2_var, from_=0, to=500, width=5)
spinbox_y2.grid(row=0, column=0, padx=5, pady=5)

# Width scale
frame_width = tk.LabelFrame(
    control_frame, text="Width:", bd=2, relief="groove", padx=5, pady=5
)
frame_width.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

scale_width = tk.Scale(
    frame_width,
    variable=width_var,
    from_=1,
    to=9,
    resolution=1,
    tickinterval=2,
    orient="horizontal",
    length=200,
    sliderlength=16,
)
scale_width.grid(row=0, column=0, padx=5, pady=5)

# Dash style combobox
frame_dash = tk.LabelFrame(
    control_frame, text="Dash:", bd=2, relief="groove", padx=5, pady=5
)
frame_dash.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

combo_dash = ttk.Combobox(
    frame_dash,
    textvariable=dash_var,
    height=5,
    values=("solid", "dashed", "dashdotted", "dotted"),
    width=15,
)
combo_dash.grid(row=0, column=0, padx=5, pady=5)

# Color combobox
frame_color = tk.LabelFrame(
    control_frame, text="Line color:", bd=2, relief="groove", padx=5, pady=5
)
frame_color.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

color_combobox = ttk.Combobox(
    frame_color,
    textvariable=fill_var,
    values=["black", "red", "blue", "green", "yellow", "purple", "orange"],
    width=15,
)
color_combobox.set("black")  # Default color
color_combobox.grid(row=0, column=0, padx=5, pady=5)

# Draw and clear buttons
button_frame = tk.Frame(control_frame)
button_frame.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

button_draw = tk.Button(
    button_frame, text="Draw", bg="orange", command=lambda: handle_draw()
)
button_draw.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

button_clear = tk.Button(
    button_frame, text="Clear", command=lambda: canvas.delete("all")
)
button_clear.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Default values
x1_var.set(0)
y1_var.set(0)
x2_var.set(100)
y2_var.set(100)
width_var.set(1)
dash_var.set("solid")
fill_var.set("black")


# Function to draw the line
def handle_draw():
    dashes = {
        "solid": None,
        "dashed": (20, 20),
        "dashdotted": (20, 5, 5, 5),
        "dotted": (5, 5),
    }
    canvas.create_line(
        x1_var.get(),
        y1_var.get(),
        x2_var.get(),
        y2_var.get(),
        width=width_var.get(),
        fill=fill_var.get(),
        dash=dashes.get(dash_var.get()),
    )


root.mainloop()
