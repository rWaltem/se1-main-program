print("delete_card starting...")
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5557")  # UI connects here

while True:
    request = socket.recv_json()
    action = request.get("action")

    if action != "delete_card":
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
    print(f"\n[Select Card to Delete from {column.title()}]")
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

    card_name, _ = cards_in_column[card_choice - 1]

    # --- Confirm deletion ---
    confirm = input(f"Are you sure you want to delete '{card_name}'? (y/N): ").strip().lower()
    if confirm != "y":
        socket.send_json({"error": "Deletion cancelled"})
        continue

    # Delete card
    col_map[column].pop(card_name)

    # --- Send updated state back ---
    socket.send_json({
        "not_started": not_started,
        "in_progress": in_progress,
        "completed": completed
    })
