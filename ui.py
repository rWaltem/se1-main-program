print("UI starting...")

from tkinter import *
import os
import zmq
import json


# global vars
set_name = "Unnamed"
not_started_cards = {}
in_progress_cards = {}
completed_cards = {}
running = True

def get_input():
    user_input = input("=: ")
    print("\n")
    return user_input.upper()

def show_menu():
    print("\n") # formatting
    print("Change set name  [C]")
    print("Save set         [S]")
    print("Load set         [L]")
    print("-----------------------")
    print("View Not Started [VN]")
    print("View In Progress [VP]")
    print("View Completed   [VC]")
    print("View All         [VA]")
    print("-----------------------")
    print("Add card         [AC]")
    print("Edit card        [EC]")
    print("Move card        [MC]")
    print("Delete card      [DC]")
    print("-----------------------")
    print("Help             [HELP]")
    print("Quit             [QUIT]")

def change_name():
    print("change name")

def save_set():
    print("save set")

def load_set():
    print("load pressed")

def view_not_started():
    print("-- Not Started --")
    if not not_started_cards:
        print(" Not cards in 'not started'")
        return

    for name, description in not_started_cards.items():
        print(f"[{name}]: {description}")


def view_in_progress():
    print("-- In Progress --")
    if not in_progress_cards:
        print(" Not cards in 'in progress'")
        return

    for name, description in in_progress_cards.items():
        print(f"[{name}]: {description}")


def view_completed():
    print("-- Completed --")
    if not completed_cards:
        print(" Not cards in 'completed'")
        return

    for name, description in completed_cards.items():
        print(f"[{name}]: {description}")


    
def view_all():
    view_not_started()
    view_in_progress()
    view_completed()

def add_card():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")  # port of add_card.py

    # send a simple request to start interaction
    socket.send_json({"action": "start_add_card"})

    # receive card info from microservice
    response = socket.recv_json()

    column = response.get("column")
    name = response.get("name")
    description = response.get("description")

    if column == "not started":
        not_started_cards[name] = description
    elif column == "in progress":
        in_progress_cards[name] = description
    elif column == "completed":
        completed_cards[name] = description
    else:
        print("Invalid column received.")

    print(f"Card added: [{column.upper()}] {name} - {description}")


def edit_card():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")  # port for edit_card.py

    # Send current data to microservice
    socket.send_json({
        "action": "edit_card",
        "not_started": not_started_cards,
        "in_progress": in_progress_cards,
        "completed": completed_cards
    })

    response = socket.recv_json()

    if "error" in response:
        print("Error:", response["error"])
        return

    old_column = response["old_column"]
    old_name = response["old_name"]
    new_name = response["new_name"]
    new_description = response["new_description"]

    # remove old entry
    if old_column == "not started":
        value = not_started_cards.pop(old_name, None)
        if value is not None:
            not_started_cards[new_name] = new_description
    elif old_column == "in progress":
        value = in_progress_cards.pop(old_name, None)
        if value is not None:
            in_progress_cards[new_name] = new_description
    elif old_column == "completed":
        value = completed_cards.pop(old_name, None)
        if value is not None:
            completed_cards[new_name] = new_description
    else:
        print("Invalid column from response")

    print(f"Card '{old_name}' updated to '{new_name}' in [{old_column}]")


def move_card():
    print("move card")

def delete_card():
    print("delete card")

def help_menu():
    print("help menu")


# main loop
def main():
    global running
    while running == True:
        # UI menu options:
        show_menu()
        o = get_input()

        if o == "C":
            change_name()
        elif o == "S":
            save_set()
        elif o == "L":
            load_set()
        elif o == "VN":
            view_not_started()
            print("\nContinue       [ENTER]")
            get_input()
        elif o == "VP":
            view_in_progress()
            print("\nContinue       [ENTER]")
            get_input()
        elif o == "VC":
            view_completed()
            print("\nContinue       [ENTER]")
            get_input()
        elif o == "VA":
            view_all()
            print("\nContinue       [ENTER]")
            get_input()
        elif o == "AC":
            add_card()
        elif o == "EC":
            edit_card()
        elif o == "MC":
            move_card()
        elif o == "DC":
            delete_card()
        elif o == "HELP":
            help_menu()
        elif o == "QUIT":
            running = False
        else:
            print("Incorrect input")
    
    print("Shutting down UI...")

if __name__ == "__main__":
    main()