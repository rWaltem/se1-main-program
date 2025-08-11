print("add_card starting...")
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")  # UI will connect to this

while True:
    request = socket.recv_json()

    if request.get("action") == "start_add_card":
        print("\n[Add Card Microservice]")

        # Column list
        col_list = ["not started", "in progress", "completed"]

        # Show numbered column choices
        print("\n[Select Column]")
        for idx, col_name in enumerate(col_list, start=1):
            print(f"{idx}. {col_name.title()}")

        try:
            col_choice = int(input("Enter column number: ").strip())
            if not (1 <= col_choice <= len(col_list)):
                socket.send_json({"error": "Invalid column selection"})
                continue
        except ValueError:
            socket.send_json({"error": "Invalid number"})
            continue

        column = col_list[col_choice - 1]

        # Get card details
        name = input("Name of card: ").strip()
        description = input("Description of card: ").strip()

        if not name:
            socket.send_json({"error": "Card name cannot be empty"})
            continue

        # Send result back to UI
        socket.send_json({
            "column": column,
            "name": name,
            "description": description
        })

    else:
        socket.send_json({"error": "Unknown action"})
