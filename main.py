import tkinter as tk
import zmq
import json
import datetime

bg_color = (255, 255, 255)
font_color = (0, 0, 0)
menu_font = 'assets/iPodSans.ttf'


def update_last_saved():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_saved_label.config(text=f"Last saved: {now}")

def save_set():
    # save to file if file is not already made
    update_last_saved()

def load_set():
    print("load pressed")

def add_card(column_frame):
    print("add new card")
    card = tk.Label(column_frame, text="New Card", relief="raised", padx=5, pady=5, bg="white")
    card.pack(pady=5, fill='x')

def edit_card():
    print("edit card")

def remove_card():
    print("remove card")

# GUI
root = tk.Tk()
root.title("Task Board")
root.geometry("800x600")

# top
top_frame = tk.Frame(root)
top_frame.pack(side="top", fill="x", padx=10, pady=5)

# top left
title_frame = tk.Frame(top_frame)
title_frame.pack(side="left", anchor="nw")

title_entry = tk.Entry(title_frame, font=(menu_font, 14), width=30)
title_entry.insert(0, "Board Name")
title_entry.pack(anchor="w")

last_saved_label = tk.Label(title_frame, text="Last saved: Never", font=(menu_font, 10))
last_saved_label.pack(anchor="w")

# top right
button_frame = tk.Frame(top_frame)
button_frame.pack(side="right", anchor="ne")

save_button = tk.Button(button_frame, text="Save", command=save_set)
save_button.pack(side="left", padx=5)

load_button = tk.Button(button_frame, text="Load", command=load_set)
load_button.pack(side="left", padx=5)

# columns
columns_frame = tk.Frame(root)
columns_frame.pack(fill="both", expand=True, padx=10, pady=10)

column_titles = ["Not Started", "In Progress", "Completed"]
column_frames = []

# cards
for title in column_titles:
    col = tk.Frame(columns_frame, bd=2, relief="groove", padx=10, pady=10)
    col.pack(side="left", fill="both", expand=True, padx=5)

    label = tk.Label(col, text=title, font=(menu_font, 12, "bold"))
    label.pack()

    content_frame = tk.Frame(col)
    content_frame.pack(fill="both", expand=True)

    add_btn = tk.Button(col, text="+", command=lambda f=content_frame: add_card(f))
    add_btn.pack(pady=5, fill='x')

    column_frames.append(content_frame)

root.mainloop()
