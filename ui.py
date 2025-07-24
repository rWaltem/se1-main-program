print("ui starting...")

from tkinter import *
import os
import zmq
import json


# global vars
not_started_cards = {}
in_progress_cards = {}
completed_cards = {}
running = True

def show_menu():
    print("\n") # formatting
    print("Change set name  [C]")
    print("Save set         [S]")
    print("Load set         [L]")
    print("--------------------")
    print("View Not Started [VN]")
    print("View In Progress [VP]")
    print("View Completed   [VC]")
    print("--------------------")
    print("Add card         [AC]")
    print("Edit card        [EC]")
    print("Move card        [MC]")
    print("Delete card      [DC]")
    print("--------------------")
    print("Clear screen     [CLEAR]")
    print("Help             [HELP]")
    print("Quit             [Q]")

def change_name():
    print("change name")

def save_set():
    print("save set")

def load_set():
    print("load pressed")

def view_not_started():
    print("view not started")

def view_in_progress():
    print("in progress")

def view_completed():
    print("completed")

def add_card():
    print("add card")

def edit_card():
    print("edit card")

def move_card():
    print("move card")

def delete_card():
    print("delete card")

def help_menu():
    print("help menu")


# main loop
def main():
    while running == True:
        # UI menu options:
        show_menu()
        user_input = input("=: ")
    
    print("Shutting down UI...")

if __name__ == "__main__":
    main()