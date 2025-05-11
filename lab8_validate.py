import tkinter as tk

subjects = [
    "Cloud Computing",
    "DevOps Fundamentals",
    "Continuous Integration and Deployment (CI/CD)",
    "Containerization with Docker",
    "Infrastructure as Code (IaC) with Terraform",
    "Monitoring and Logging",
    "Cybersecurity Basics",
    "Machine Learning",
    "Artificial Intelligence",
    "Mobile App Development",
    "Frontend Frameworks (React, Angular)",
    "Backend Development with Node.js",
    "APIs and Web Services",
    "Shell Scripting",
    "Python for Automation",
    "Agile and Scrum Methodologies",
    "Microservices Architecture",
    "Testing and Debugging",
    "Virtualization with KVM/QEMU",
    "Cloud Providers (AWS, Azure, GCP)"
]

root = tk.Tk()
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

# Labels
label_subject = tk.Label(text="Subject:", width=20)
label_subject.grid(row=0, column=0)

label_surname = tk.Label(text="Surname:", width=20)
label_surname.grid(row=0, column=1)

label_semester = tk.Label(text="Semester number:", width=20)
label_semester.grid(row=0, column=2)

# Functions
def on_keyrelease(event):
    value = entry.get().strip().lower()
    listbox.delete(0, tk.END)
    if value == "":
        listbox.grid_remove()
        return
    matches = [subject for subject in subjects if subject.lower().startswith(value)]
    if matches:
        listbox.grid()
        for subject in matches[:3]:
            listbox.insert("end", subject)
    else:
        listbox.grid_remove()

def on_listbox_select(event):
    if listbox.curselection():
        selected = listbox.get(listbox.curselection())
        entry.config(validate="none")
        entry.delete(0, tk.END)
        entry.insert(0, selected)
        entry.config(validate="key")
        listbox.delete(0, tk.END)
        listbox.grid_remove()
        surname_entry.focus_set()

def validate_subject(symbol):
    return symbol.isalnum() or symbol in [" ", "-", "(", ")", ".", ","]

def invalid_subject():
    label_status.config(
        fg="red",
        text="Subject: Only letters, numbers, spaces, commas, dashes, and parentheses allowed"
    )

entry_vcmd = root.register(validate_subject)
entry_invcmd = root.register(invalid_subject)

entry = tk.Entry(
    validate="key",
    validatecommand=(entry_vcmd, "%S"),
    invalidcommand=entry_invcmd,
)
entry.grid(row=1, column=0, sticky="we", padx=5, pady=5)

def validate_semester(semester):
    return semester.isdecimal() or semester == ""

def invalid_semester():
    label_status.config(
        fg="red",
        text="Semester: number only 1-8"
    )

def validate_surname(value):
    return len(value) <= 20

def invalid_surname():
    label_status.config(
        fg="red",
        text="Surname: max 20 characters"
    )

spinbox_vcmd = root.register(validate_semester)
spinbox_invcmd = root.register(invalid_semester)
surname_vcmd = root.register(validate_surname)
surname_invcmd = root.register(invalid_surname)

# Surname entry (column 1)
surname_entry = tk.Entry(
    validate="key",
    validatecommand=(surname_vcmd, "%P"),
    invalidcommand=surname_invcmd,
)
surname_entry.grid(row=1, column=1, sticky="we", padx=5, pady=5)

spinbox = tk.Spinbox(
    from_=1,
    to=8,
    increment=1,
    validate="all",
    validatecommand=(spinbox_vcmd, "%P"),
    invalidcommand=spinbox_invcmd,
)
spinbox.grid(row=1, column=2, sticky="we", padx=5, pady=5)

listbox = tk.Listbox(height=3)
listbox.grid(row=2, column=0, sticky="we", padx=5, pady=5)
listbox.grid_remove()

def handle_button():
    subject = entry.get()
    semester = int(spinbox.get())
    if subject not in subjects:
        label_status.config(fg="red", text=f"Wrong subject")
        return
    if not (1 <= semester <= 8):
        label_status.config(fg="red", text=f"Wrong semester")
        return
    label_status.config(
        fg="black",
        text=f"Subject: {entry.get()}, Surname: {surname_entry.get()}, semester: {spinbox.get()}"
    )

button = tk.Button(
    text="Send Form",
    command=handle_button,
)
button.grid(row=3, column=0, columnspan=2)

label_status = tk.Label(anchor="w")
label_status.grid(row=4, column=0, columnspan=2, sticky="we")

entry.bind("<KeyRelease>", on_keyrelease)
listbox.bind("<<ListboxSelect>>", on_listbox_select)
entry.focus_set()

root.mainloop()