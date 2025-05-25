import tkinter as tk
from tkinter import font as tkfont
import datetime

# Initialize main window
root = tk.Tk()
root.title("Chat Bot")
root.geometry("400x500")
root.minsize(300, 300)
root.configure(bg="#f0f0f0")

# Fonts
message_font = tkfont.Font(family="Helvetica", size=10)
header_font = tkfont.Font(family="Helvetica", size=10, weight="bold")

# Case sensitivity toggle
case_var = tk.BooleanVar(value=False)

# Title frame
frame_title = tk.Frame(root, bg="#4a7abc", pady=10)
frame_title.pack(fill="x")
tk.Label(
    frame_title,
    text="Chat Bot",
    font=("Helvetica", 14, "bold"),
    fg="white",
    bg="#4a7abc",
).pack()

# Text display frame
frame_text = tk.Frame(bg="#f0f0f0")
frame_text.pack(fill="both", expand=True, padx=10, pady=10)

scroll = tk.Scrollbar(frame_text)
scroll.pack(side="right", fill="y")

text_widget = tk.Text(
    frame_text,
    width=35,
    wrap="word",
    yscrollcommand=scroll.set,
    state="disabled",
    font=message_font,
    bg="white",
    bd=1,
    relief="solid",
)
text_widget.pack(side="left", fill="both", expand=True)
scroll.config(command=text_widget.yview)

# Text tags
text_widget.tag_config("highlight", foreground="yellow", background="#333333")
text_widget.tag_config("green", background="#e6ffe6")
text_widget.tag_config("blue", background="#e6f2ff")
text_widget.tag_config("user", font=header_font, foreground="#006600")
text_widget.tag_config("bot", font=header_font, foreground="#003366")

# Message sending frame
frame_send = tk.Frame(root, bg="#f0f0f0")
frame_send.pack(fill="x", padx=10, pady=(0, 10))

id_message = 0
messages = [
    "Яке місце ти б хотів(-ла) відвідати?",
    "Які враження залишилися від останньої поїздки?",
    "Чи любиш більше активний відпочинок чи спокійне проведення часу?",
    "Яка поїздка справила на тебе найбільше враження?",
    "Чи були подорожі, які змінили твоє бачення світу або себе?",
    "Які країни або міста є в твоєму списку бажаних подорожей?",
    "Чи плануєш якісь поїздки найближчим часом?",
    "Які незвичні страви тобі доводилося куштувати під час мандрів?",
    "Що для тебе найважливіше в подорожах — культура, природа, люди чи відпочинок?",
    "Які корисні звички або інсайти ти привіз(-ла) з подорожей?",
]


def create_line(tag, text):
    text_widget.config(state="normal")
    # Timestamp for headers
    if text == "You:" or text == "ChatGPT-5":
        current_time = datetime.datetime.now().strftime("%H:%M")
        display_text = f"{text} [{current_time}]"
    else:
        display_text = text

    if tag == "green":
        if display_text.startswith("You:"):
            text_widget.insert(tk.END, f"{display_text}\n", "user")
        else:
            text_widget.insert(tk.END, f"{display_text}\n", tag)
    elif tag == "blue":
        if display_text.startswith("ChatGPT-5"):
            text_widget.insert(tk.END, f"{display_text}\n", "bot")
        else:
            text_widget.insert(tk.END, f"{display_text}\n", tag)
    else:
        text_widget.insert(tk.END, f"{display_text}\n", tag)

    text_widget.yview_moveto(1.0)
    text_widget.config(state="disabled")


def handle_send():
    global id_message
    post = entry_send.get()
    if not post.strip():
        return
    create_line("green", "You:")
    create_line("green", post)
    entry_send.delete(0, tk.END)
    create_line("blue", "ChatGPT-5")
    if id_message >= len(messages):
        create_line("blue", "Я втомився, поговоримо пізніше...")
        return
    create_line("blue", messages[id_message])
    id_message += 1


# Entry frame
entry_frame = tk.Frame(frame_send, bg="#dddddd", bd=1, relief="solid")
entry_frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)

entry_send = tk.Entry(entry_frame, width=62, bd=0, font=message_font)
entry_send.pack(side="left", fill="x", expand=True, padx=5, pady=5)

button_send = tk.Button(
    frame_send,
    width=10,
    text="Send",
    bg="#4a7abc",
    fg="white",
    command=handle_send,
    relief="flat",
)
button_send.pack(side="left", padx=5, pady=5)

button_clear = tk.Button(
    frame_send,
    width=10,
    text="Clear Chat",
    bg="#f44336",
    fg="white",
    command=lambda: clear_chat(),
    relief="flat",
)
button_clear.pack(side="left", padx=5, pady=5)

# Search frame
frame_find = tk.Frame(root, bg="#f0f0f0")
frame_find.pack(fill="x", padx=10, pady=(0, 10))

search_frame = tk.Frame(frame_find, bg="#dddddd", bd=1, relief="solid")
search_frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)

entry_search = tk.Entry(search_frame, bd=0, font=message_font)
entry_search.pack(side="left", fill="x", expand=True, padx=5, pady=5)

label_case = tk.Label(frame_find, text="Match case:", bg="#f0f0f0")
label_case.pack(side="left", pady=5)

check_case = tk.Checkbutton(frame_find, variable=case_var, bg="#f0f0f0")
check_case.pack(side="left", pady=5)


def handle_find_all():
    text_widget.tag_raise("highlight")
    text_widget.config(state="normal")
    text_widget.tag_remove("highlight", "1.0", "end")

    pattern = entry_search.get()
    if not pattern:
        return

    index = "1.0"
    stopindex = "end"
    while True:
        position = text_widget.search(
            pattern,
            index=index,
            stopindex=stopindex,
            nocase=not case_var.get(),
        )
        if position:
            start = position
            finish = f"{start}+{len(pattern)}c"
            text_widget.tag_add("highlight", start, finish)
            index = finish
        else:
            break

    text_widget.config(state="disabled")


button_find = tk.Button(
    frame_find,
    width=10,
    text="Find All",
    bg="#4a7abc",
    fg="white",
    command=handle_find_all,
    relief="flat",
)
button_find.pack(side="left", padx=5, pady=5)

entry_send.bind("<KeyPress-Return>", lambda e: handle_send())
root.bind("<KeyPress>", lambda e: text_widget.tag_remove("highlight", "1.0", "end"))


def clear_chat():
    global id_message
    text_widget.config(state="normal")
    text_widget.delete("1.0", tk.END)
    text_widget.config(state="disabled")
    id_message = 0
    create_line("blue", "ChatGPT-5:")
    create_line("blue", "Привіт! Як справи?")


# Status bar
status_frame = tk.Frame(root, bg="#e0e0e0", height=20)
status_frame.pack(fill="x", side="bottom")
status_label = tk.Label(status_frame, text="Ready", bg="#e0e0e0", anchor="w", padx=10)
status_label.pack(fill="x")

# Initial greeting
create_line("blue", "ChatGPT-5")
create_line("blue", "Привіт! Як справи?")
entry_send.focus_set()

root.mainloop()
