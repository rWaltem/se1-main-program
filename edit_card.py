print("edit_card starting...")
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556") # UI will connect to this

while True:
    request = socket.recv_json()

    if request.get("action") == "edit_card":
        print("\n[Edit Card Microservice]")

        # show all cards
        for col in ["not_started", "in_progress", "completed"]:
            print(f"\n-- {col.replace('_', ' ').title()} --")
            for name, desc in request[col].items():
                print(f"[{name}]: {desc}")

        # get column and card
        col_map = {
            "not started": "not_started",
            "in progress": "in_progress",
            "completed": "completed"
        }

        column = input("\nWhich column is the card in? ").strip().lower()
        if column not in col_map:
            socket.send_json({"error": "Invalid column"})
            continue

        card_name = input("Which card do you want to edit? ").strip()

        cards = request[col_map[column]]
        if card_name not in cards:
            socket.send_json({"error": "Card not found in selected column"})
            continue

        # get new data
        new_name = input("New name (press Enter to keep the same): ").strip()
        new_description = input("New description (press Enter to keep the same): ").strip()

        if new_name == "":
            new_name = card_name
        if new_description == "":
            new_description = cards[card_name]

        socket.send_json({
            "old_column": column,
            "old_name": card_name,
            "new_name": new_name,
            "new_description": new_description
        })
    else:
        socket.send_json({"error": "Unknown action"})
