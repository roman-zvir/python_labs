import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import sqlite3
import csv

DB_FILE = "contacts.sqlite3"

# --- Database helpers ------------------------------------------------------


def db_init():
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS contacts(
            name TEXT,
            experience TEXT,
            department TEXT
        )"""
        )
        con.commit()


def db_set(contacts):
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM contacts")
        cur.executemany("INSERT INTO contacts VALUES(?, ?, ?)", contacts)
        con.commit()


def db_get():
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM contacts")
        return cur.fetchall()


# --- CSV import/export -----------------------------------------------------


def csv_export(contacts):
    if not contacts:
        return
    path = filedialog.asksaveasfilename(
        title="Export to CSV",
        defaultextension=".csv",
        filetypes=[("CSV", "*.csv"), ("All", "*.*")],
    )
    if not path:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(contacts)


def csv_import():
    path = filedialog.askopenfilename(
        title="Import from CSV", filetypes=[("CSV", "*.csv"), ("All", "*.*")]
    )
    if not path:
        return []
    valid = []
    skipped = 0
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 3 and validate(row[0], row[1], row[2]):
                entry = (row[0].strip(), row[1].strip(), row[2].strip())
                if entry not in valid:
                    valid.append(entry)
                else:
                    skipped += 1
            else:
                skipped += 1
    if skipped:
        messagebox.showwarning("Import", f"Skipped {skipped} invalid row(s).")
    return valid


# --- TreeView helpers ------------------------------------------------------

sort_dir = {}


def sort_column(tv, col):
    data = [(tv.set(k, col), k) for k in tv.get_children("")]
    ascending = sort_dir.get(col, True)
    data.sort(reverse=not ascending)
    for index, (_, k) in enumerate(data):
        tv.move(k, "", index)
    sort_dir[col] = not ascending


def refresh_tree(filter_text=""):
    tree.delete(*tree.get_children())
    for name, experience, department in db_get():
        if (
            filter_text.lower() in name.lower()
            or filter_text.lower() in experience.lower()
            or filter_text.lower() in department.lower()
        ):
            tree.insert("", "end", values=(name, experience, department))


def get_selected():
    sel = tree.selection()
    return sel[0] if sel else None


# --- Validation & Dialog ---------------------------------------------------


def validate(name, experience, department):
    if not name.strip():
        messagebox.showerror("Validation", "Name cannot be empty.")
        return False
    if not experience.strip():
        messagebox.showerror("Validation", "Experience cannot be empty.")
        return False
    if not department.strip():
        messagebox.showerror("Validation", "Department cannot be empty.")
        return False
    return True


class ContactDialog(simpledialog.Dialog):
    def __init__(self, parent, title, name="", experience="", department=""):
        self.init_name = name
        self.init_experience = experience
        self.init_department = department
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Name:").grid(row=0, column=0, sticky="e")
        tk.Label(master, text="Experience:").grid(row=1, column=0, sticky="e")
        tk.Label(master, text="Department:").grid(row=2, column=0, sticky="e")
        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)
        self.e3 = tk.Entry(master)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e1.insert(0, self.init_name)
        self.e2.insert(0, self.init_experience)
        self.e3.insert(0, self.init_department)
        return self.e1

    def apply(self):
        name, experience, department = self.e1.get(), self.e2.get(), self.e3.get()
        if validate(name, experience, department):
            self.result = (name.strip(), experience.strip(), department.strip())


# --- CRUD operations -------------------------------------------------------


def add_contact():
    dlg = ContactDialog(root, "Add Contact")
    if dlg.result:
        contacts = db_get() + [dlg.result]
        db_set(contacts)
        refresh_tree(search_var.get())


def edit_contact():
    sel = get_selected()
    if not sel:
        return
    old_values = tree.item(sel, "values")
    dlg = ContactDialog(root, "Edit Contact", *old_values)
    if dlg.result:
        contacts = db_get()
        if tuple(old_values) in contacts:
            idx = contacts.index(tuple(old_values))
            contacts[idx] = dlg.result
            db_set(contacts)
            refresh_tree(search_var.get())


def delete_contact():
    sel = get_selected()
    if not sel:
        return
    if not messagebox.askyesno("Confirm", "Delete selected?"):
        return
    val = tuple(tree.item(sel, "values"))
    contacts = db_get()
    if val in contacts:
        contacts.remove(val)
        db_set(contacts)
    refresh_tree(search_var.get())


drag_data = {"item": None}


def on_start_drag(event):
    """Begin drag: remember the item under the cursor."""
    item = tree.identify_row(event.y)
    if item:
        drag_data["item"] = item


def on_drop(event):
    """On drop, reorder the contacts list and refresh."""
    src = drag_data["item"]
    if not src:
        return
    dst = tree.identify_row(event.y)
    if dst and dst != src:
        contacts = db_get()
        src_idx = tree.index(src)
        dst_idx = tree.index(dst)
        entry = contacts.pop(src_idx)
        contacts.insert(dst_idx, entry)
        db_set(contacts)
        refresh_tree(search_var.get())
        # re-select the moved item
        children = tree.get_children()
        tree.selection_set(children[dst_idx])
    drag_data["item"] = None


# optional: give visual feedback during drag
def on_drag(event):
    pass


def move(up=True):
    sel = get_selected()
    if not sel:
        return
    contacts = db_get()
    idx = tree.index(sel)
    new_idx = idx - 1 if up else idx + 1
    if 0 <= new_idx < len(contacts):
        contacts[idx], contacts[new_idx] = contacts[new_idx], contacts[idx]
        db_set(contacts)
        refresh_tree(search_var.get())
        children = tree.get_children()
        tree.selection_set(children[new_idx])


def clean_db():
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        # Delete rows where any of the three expected fields is NULL or empty string
        cur.execute(
            """
            DELETE FROM contacts
            WHERE name IS NULL OR name = ''
               OR experience IS NULL OR experience = ''
               OR department IS NULL OR department = ''
        """
        )
        con.commit()


# --- Build UI --------------------------------------------------------------

root = tk.Tk()
root.title("Contacts Manager")
root.geometry("600x400")

frm_search = tk.Frame(root)
frm_search.pack(fill="x", padx=5, pady=2)
search_var = tk.StringVar()
tk.Label(frm_search, text="Search:").pack(side="left")
tk.Entry(frm_search, textvariable=search_var).pack(side="left", fill="x", expand=True)
tk.Button(frm_search, text="Go", command=lambda: refresh_tree(search_var.get())).pack(
    side="left", padx=2
)
tk.Button(
    frm_search, text="Clear", command=lambda: (search_var.set(""), refresh_tree(""))
).pack(side="left")

frm = tk.Frame(root)
frm.pack(fill="both", expand=True, padx=5, pady=5)
tree = ttk.Treeview(frm, columns=("Name", "Experience", "Department"), show="headings")
ysb = ttk.Scrollbar(frm, orient="vertical", command=tree.yview)
tree.configure(yscroll=ysb.set)
tree.heading("Name", text="Name", command=lambda: sort_column(tree, "Name"))
tree.heading(
    "Experience", text="Experience", command=lambda: sort_column(tree, "Experience")
)
tree.heading(
    "Department", text="Department", command=lambda: sort_column(tree, "Department")
)
tree.column("Name", anchor="w", width=150)
tree.column("Experience", anchor="w", width=100)
tree.column("Department", anchor="w", width=150)
tree.pack(side="left", fill="both", expand=True)
ysb.pack(side="left", fill="y")

frm_btns = tk.Frame(root)
frm_btns.pack(fill="x", padx=5, pady=5)
for txt, cmd in [
    ("Add", add_contact),
    ("Edit", edit_contact),
    ("Delete", delete_contact),
    ("Up", lambda: move(True)),
    ("Down", lambda: move(False)),
    ("Import", lambda: (db_set(csv_import()), refresh_tree(search_var.get()))),
    ("Export", lambda: csv_export(db_get())),
]:
    tk.Button(frm_btns, text=txt, command=cmd).pack(side="left", padx=2)

tree.bind("<Double-1>", lambda e: edit_contact())
root.bind("<Delete>", lambda e: delete_contact())
root.bind("<Control-Up>", lambda e: move(True))
root.bind("<Control-Down>", lambda e: move(False))
tree.bind("<ButtonPress-1>", on_start_drag)
root.bind("<Alt-Up>", lambda e: move(True))
root.bind("<Alt-Down>", lambda e: move(False))
tree.bind("<B1-Motion>", on_drag)
tree.bind("<ButtonRelease-1>", on_drop)


if __name__ == "__main__":
    db_init()
    clean_db()
    refresh_tree()
    root.mainloop()
