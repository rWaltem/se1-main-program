print("add_card starting...")
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")  # UI will connect to this

while True:
    request = socket.recv_json()
    
    if request.get("action") == "start_add_card":
        print("\n[Add Card Microservice]")

        # Prompt user for card details
        column = input("Which column? [not started / in progress / completed]: ").strip().lower()
        name = input("Name of card: ").strip()
        description = input("Description of card: ").strip()

        # Send result back to UI
        socket.send_json({
            "column": column,
            "name": name,
            "description": description
        })
    else:
        socket.send_json({"error": "Unknown action"})

