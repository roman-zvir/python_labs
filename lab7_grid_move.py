import tkinter as tk

# Constants
grid_spacing = 40
oval_width = 30
oval_height = 30

# Global variables
figure_x = 0
figure_y = 0

# Root window setup
root = tk.Tk()
root.title("Grid Drawing Application")
root.geometry("755x545")
root.minsize(395, 345)

# Main frame and canvas setup
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(main_frame, bg="white", bd=2, relief="groove")
canvas.pack(fill="both", expand=True, padx=5, pady=5)

label = tk.Label(root, anchor="w", text="Start", bd=1, relief="sunken", padx=10)
label.pack(fill="x", expand=False, side="bottom", padx=5, pady=5)

# Initial figure placement
cell_center_x = grid_spacing / 2
cell_center_y = grid_spacing / 2
figure = canvas.create_oval(
    cell_center_x - oval_width / 2,
    cell_center_y - oval_height / 2,
    cell_center_x + oval_width / 2,
    cell_center_y + oval_height / 2,
    width=0,
    fill="black",
)


# Functions
def draw_grid():
    canvas.delete("grid")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    for x in range(0, width, grid_spacing):
        canvas.create_line(x, 0, x, height, fill="lightgray", tags="grid")
    for y in range(0, height, grid_spacing):
        canvas.create_line(0, y, width, y, fill="lightgray", tags="grid")


def handle_resize(event):
    draw_grid()


def show_coords(event):
    label.config(text=f"x: {event.x}, y: {event.y}")


def handle_up(event):
    x1, y1, x2, y2 = canvas.coords(figure)
    dy = -grid_spacing if (y1 > grid_spacing) else 0
    canvas.move(figure, 0, dy)


def handle_down(event):
    x1, y1, x2, y2 = canvas.coords(figure)
    y_max = canvas.winfo_height()
    dy = grid_spacing if (y1 < y_max - grid_spacing) else 0
    canvas.move(figure, 0, dy)


def handle_left(event):
    x1, y1, x2, y2 = canvas.coords(figure)
    dx = -grid_spacing if (x1 > grid_spacing) else 0
    canvas.move(figure, dx, 0)


def handle_right(event):
    x1, y1, x2, y2 = canvas.coords(figure)
    x_max = canvas.winfo_width()
    dx = grid_spacing if (x2 < x_max - grid_spacing) else 0
    canvas.move(figure, dx, 0)


def handle_start_drag(event):
    global figure_x, figure_y
    figure_x = event.x
    figure_y = event.y
    canvas.itemconfig(figure, width=2)
    canvas.config(cursor="hand2")
    canvas.tag_raise(figure)


def handle_on_drag(event):
    global figure_x, figure_y
    dx = event.x - figure_x
    dy = event.y - figure_y
    canvas.move(figure, dx, dy)
    figure_x = event.x
    figure_y = event.y


def handle_end_drag(event):
    global figure_x, figure_y
    canvas.itemconfig(figure, width=0)
    canvas.config(cursor="arrow")
    x1, y1, x2, y2 = canvas.coords(figure)
    width = x2 - x1
    height = y2 - y1
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    n_x = round((center_x - grid_spacing / 2) / grid_spacing)
    n_y = round((center_y - grid_spacing / 2) / grid_spacing)
    cell_center_x = n_x * grid_spacing + grid_spacing / 2
    cell_center_y = n_y * grid_spacing + grid_spacing / 2
    new_x1 = cell_center_x - width / 2
    new_y1 = cell_center_y - height / 2
    canvas.coords(figure, new_x1, new_y1, new_x1 + width, new_y1 + height)
    figure_x = 0
    figure_y = 0


# Event bindings
canvas.bind("<Configure>", handle_resize)
canvas.bind("<Motion>", show_coords)
root.bind("<KeyPress-Up>", handle_up)
root.bind("<KeyPress-Down>", handle_down)
root.bind("<KeyPress-Left>", handle_left)
root.bind("<KeyPress-Right>", handle_right)
canvas.tag_bind(figure, "<Button-1>", handle_start_drag)
canvas.tag_bind(figure, "<B1-Motion>", handle_on_drag)
canvas.tag_bind(figure, "<ButtonRelease-1>", handle_end_drag)

# Main loop
root.mainloop()
