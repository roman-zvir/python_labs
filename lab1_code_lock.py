import tkinter as tk

root = tk.Tk()
root.title("Code lock")
root.resizable(width=False, height=False)

frame_display = tk.Frame(root, bg="Black")
frame_display.pack(fill="x", padx=5, pady=5)

label_display = tk.Label(frame_display, bg="White", font=("Arial", 14))
label_display.pack(fill="x", padx=2, pady=2)

frame_keyboard = tk.Frame(root)
frame_keyboard.pack(fill="both", padx=5, pady=5)

CORRECT_CODE = "6943"
code = ""

def handle_digit(digit):
    global code
    if len(code) >= 6:
        return
    code += digit
    label_display.config(text=code, fg="black")

def handle_back():
    global code
    code = ""
    label_display.config(text=code)

def handle_enter():
    global code
    if code == CORRECT_CODE:
        label_display.config(text="Вірно!", fg="green")
    else:
        label_display.config(text="Невірно!", fg="red")
    code = ""

# Digit buttons
buttons = [
    ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
    ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
    ("0", 3, 1)
]

for (text, row, col) in buttons:
    button = tk.Button(frame_keyboard, width=5, text=text, command=lambda t=text: handle_digit(t))
    button.grid(row=row, column=col, padx=2, pady=2)

# Control buttons
button_back = tk.Button(frame_keyboard, width=5, text="Clear", bg="blue", command=handle_back)
button_back.grid(row=3, column=0, padx=2, pady=2)

button_enter = tk.Button(frame_keyboard, width=5, text="Enter", bg="green", command=handle_enter)
button_enter.grid(row=3, column=2, padx=2, pady=2)

root.mainloop()
