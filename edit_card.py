print("edit_card starting...")
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")  # UI connects here

while True:
    request = socket.recv_json()
    action = request.get("action")

    if action not in ("edit_card", "move_card"):
        socket.send_json({"error": "Unknown action"})
        continue

    # Extract board state
    not_started = request["not_started"]
    in_progress = request["in_progress"]
    completed = request["completed"]

    col_map = {
        "not started": not_started,
        "in progress": in_progress,
        "completed": completed
    }
    col_list = list(col_map.keys())

    # --- Pick a column ---
    print("\n[Select Column]")
    for idx, col_name in enumerate(col_list, start=1):
        print(f"{idx}. {col_name.title()} ({len(col_map[col_name])} cards)")

    try:
        col_choice = int(input("Enter column number: ").strip())
        if not (1 <= col_choice <= len(col_list)):
            socket.send_json({"error": "Invalid column selection"})
            continue
    except ValueError:
        socket.send_json({"error": "Invalid number"})
        continue

    column = col_list[col_choice - 1]
    cards_in_column = list(col_map[column].items())

    if not cards_in_column:
        socket.send_json({"error": f"No cards in '{column}'"})
        continue

    # --- Pick a card ---
    print(f"\n[Select Card from {column.title()}]")
    for idx, (name, desc) in enumerate(cards_in_column, start=1):
        print(f"{idx}. {name}: {desc}")

    try:
        card_choice = int(input("Enter card number: ").strip())
        if not (1 <= card_choice <= len(cards_in_column)):
            socket.send_json({"error": "Invalid card selection"})
            continue
    except ValueError:
        socket.send_json({"error": "Invalid number"})
        continue

    card_name, card_desc = cards_in_column[card_choice - 1]

    # --- Edit / Move Logic ---
    if action == "edit_card":
        print("\nWhat would you like to change?")
        print("1. Name")
        print("2. Description")
        print("3. Column")
        print("4. Name & Description")
        print("5. Name & Column")
        print("6. Description & Column")
        print("7. Name, Description & Column")

        try:
            choice = int(input("Enter choice number: ").strip())
            if not (1 <= choice <= 7):
                socket.send_json({"error": "Invalid choice"})
                continue
        except ValueError:
            socket.send_json({"error": "Invalid number"})
            continue

        new_name = card_name
        new_description = card_desc
        new_column = column

        if choice in (1, 4, 5, 7):
            temp = input(f"New name (leave blank to keep '{card_name}'): ").strip()
            if temp:
                new_name = temp

        if choice in (2, 4, 6, 7):
            temp = input("New description (leave blank to keep existing): ").strip()
            if temp:
                new_description = temp

        if choice in (3, 5, 6, 7):
            print("\n[Select New Column]")
            for idx, col_name in enumerate(col_list, start=1):
                print(f"{idx}. {col_name.title()}")
            try:
                new_col_choice = int(input("Enter new column number: ").strip())
                if not (1 <= new_col_choice <= len(col_list)):
                    socket.send_json({"error": "Invalid column selection"})
                    continue
            except ValueError:
                socket.send_json({"error": "Invalid number"})
                continue
            new_column = col_list[new_col_choice - 1]

        # Apply changes
        col_map[column].pop(card_name)
        col_map[new_column][new_name] = new_description

    elif action == "move_card":
        print("\n[Select New Column]")
        for idx, col_name in enumerate(col_list, start=1):
            print(f"{idx}. {col_name.title()}")

        try:
            new_col_choice = int(input("Enter new column number: ").strip())
            if not (1 <= new_col_choice <= len(col_list)):
                socket.send_json({"error": "Invalid column selection"})
                continue
        except ValueError:
            socket.send_json({"error": "Invalid number"})
            continue

        new_column = col_list[new_col_choice - 1]
        col_map[column].pop(card_name)
        col_map[new_column][card_name] = card_desc

    # --- Send updated state back ---
    socket.send_json({
        "not_started": not_started,
        "in_progress": in_progress,
        "completed": completed
    })
