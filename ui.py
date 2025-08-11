print("UI starting...")

from tkinter import *
import zmq
import json
import os


# global vars
set_name = "Unnamed"
user_name = "Unknown"
not_started_cards = {}
in_progress_cards = {}
completed_cards = {}
running = True

context = zmq.Context()

def get_input():
    user_input = input("=: ")
    print("\n")
    return user_input.upper()

def show_menu():
    global set_name, user_name

    print("\n")
    print(f"Username: {user_name}")
    print(f"Set name: {set_name}")
    print("------------------------")
    print("Change set name  [C]")
    print("Change username  [U]")
    print("Save set         [S]")
    print("Load set         [L]")
    print("------------------------")
    print("View Not Started [VN]")
    print("View In Progress [VP]")
    print("View Completed   [VC]")
    print("View All         [VA]")
    print("------------------------")
    print("Add card         [AC]")
    print("Edit card        [EC]")
    print("Move card        [MC]")
    print("Delete card      [DC]")
    print("------------------------")
    print("Clear terminal   [CLEAR]")
    print("Quit             [QUIT]")

def change_name():
    global set_name
    print(f"Current set name: {set_name}")
    new_name = input("New name: ")
    
    # user can press enter to not change name
    if new_name == "":
        return
    
    set_name = new_name

def change_set_name():
    global user_name
    print(f"Current username: {user_name}")
    new_username = input("New username: ")
    
    # user can press enter to not change name
    if new_username == "":
        return
    
    user_name = new_username

def save_set():
    global set_name, user_name

    if set_name == "Unnamed":
        set_name = input("Name current board? New name (Press enter for no): ")

    if user_name == "Unknown":
        user_name = input("Change username? Type your new name (Press enter for no): ")

    board_name = set_name
    user_name = user_name

    if board_name == "":
        print("Error: No name given")
        return
        

    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5655")  # port of microservice_a

    file_data = {
        "action": "save",
        "board_id": board_name,
        "user_id": user_name,
        "data":
        {
            "board-name": set_name,
            "not-started": not_started_cards,
            "in-progress": in_progress_cards,
            "completed": completed_cards
        }
    }

    # send card sets
    socket.send_json(file_data)

    response = socket.recv_json()
    print(response)


def load_set():
    global not_started_cards, in_progress_cards, completed_cards, set_name

    board_path = input("What is the board name? ")

    if board_path == "":
        print("Error: No name given")
        return
    
    # checks if the file path leads to a file
    if os.path.isfile(board_path) == False:
        print("Error: file does not exist")
        return

    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5655")  # port of microservice_a

    request = {
        "action": "load",
        "file_name": board_path
    }

    socket.send_json(request)

    response = socket.recv_json()
    data = response["data"]

    if not data["board-name"]:
        set_name = "Unnamed"
    else:
        set_name = data["board-name"]

    not_started_cards = data["not-started"]
    in_progress_cards = data["in-progress"]
    completed_cards = data["completed"]

    print("Loaded card set")

def view_not_started():
    print("-- Not Started --")
    if not not_started_cards:
        print(" No cards in 'not started'")
        return

    for name, description in not_started_cards.items():
        print(f"[{name}]: {description}")


def view_in_progress():
    print("-- In Progress --")
    if not in_progress_cards:
        print(" No cards in 'in progress'")
        return

    for name, description in in_progress_cards.items():
        print(f"[{name}]: {description}")


def view_completed():
    print("-- Completed --")
    if not completed_cards:
        print(" No cards in 'completed'")
        return

    for name, description in completed_cards.items():
        print(f"[{name}]: {description}")


    
def view_all():
    view_not_started()
    view_in_progress()
    view_completed()

def add_card():  
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
    global not_started_cards, in_progress_cards, completed_cards
    
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")

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

    not_started_cards = response["not_started"]
    in_progress_cards = response["in_progress"]
    completed_cards = response["completed"]

    print("Card edited successfully.")


def move_card():
    global not_started_cards, in_progress_cards, completed_cards
    
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")

    socket.send_json({
        "action": "move_card",
        "not_started": not_started_cards,
        "in_progress": in_progress_cards,
        "completed": completed_cards
    })

    response = socket.recv_json()
    if "error" in response:
        print("Error:", response["error"])
        return

    not_started_cards = response["not_started"]
    in_progress_cards = response["in_progress"]
    completed_cards = response["completed"]

    print("Card moved successfully.")

def delete_card():
    global not_started_cards, in_progress_cards, completed_cards
    
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5557")

    socket.send_json({
        "action": "delete_card",
        "not_started": not_started_cards,
        "in_progress": in_progress_cards,
        "completed": completed_cards
    })

    response = socket.recv_json()

    if "error" in response:
        print("Error:", response["error"])
    else:
        # update local state
        not_started_cards = response["not_started"]
        in_progress_cards = response["in_progress"]
        completed_cards = response["completed"]
        print("Card deleted successfully!")


def help_menu():
    print("help menu")

    
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


# main loop
def main():
    global running
    while running == True:
        # UI menu options:
        show_menu()
        o = get_input()

        if o == "C":
            change_name()
        elif o == "U":
            change_set_name()
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
        elif o == "CLEAR":
            clear_terminal()
        elif o == "QUIT" or o == "EXIT":
            running = False
        else:
            print("Incorrect input")
    
    print("Shutting down UI...")

if __name__ == "__main__":
    main()