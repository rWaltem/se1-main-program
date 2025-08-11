"""
Citations:
1. GeeksforGeeks:
   https://www.geeksforgeeks.org/python/read-json-file-using-python/
   -Used as reference for reading and writing JSON files in Python.

2. ZeroMQ:
   https://zeromq.org/get-started/?language=python&library=pyzmq#
   -Used as reference for implementing ZeroMQ REQ/REP communication.
"""

import time

# import field
import zmq # need dependency for this
import json

# credit: https://zeromq.org/get-started/?language=python&library=pyzmq#

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5655")

while True:
    #  Wait for next request from client
    try: message = socket.recv_json()

    except ValueError:
        socket.send_json({"error": "Invalid request- could not receive message."})

    # get the request type
    action = message["action"]

    # if user wanted to save their file:
    if action == "save":

        # make sure file has correct data needed
        required_values = ["action", "user_id", "board_id", "data"]
        missing_values = [field for field in required_values if field not in message]

        if missing_values:
            socket.send_json({"error": "Missing fields."})
            continue

        # use the required values to make a new filename
        user_id = message["user_id"]
        board_id = message["board_id"]
        file_name = f"{user_id}_{board_id}.json"

        # get the data
        data = message["data"]

        # Open and write the JSON file
        with open(file_name, 'w') as f:
            json.dump(data, f)

        #  Do some 'work'
        time.sleep(1)

        #  Send reply back to client
        socket.send_json({"status": "saved", "file_name": file_name})

    # if user wanted to retrieve their saved file:
    elif action == "load":

        # make sure file has correct data needed
        required_values = ["action", "file_name"]
        missing_values = [field for field in required_values if field not in message]
        if missing_values:
            socket.send_json({"error": "Missing fields."})
            continue

        # get the file name1
        file_name = message["file_name"]

        # read from file and turn into json
        try:
            with open (file_name, "r") as f:
                board_data = json.load(f)
        except:
            socket.send_json({"error": "File not found."})
            continue

        socket.send_json({"status": "loaded", "data": board_data})

    else:
        socket.send_json({"error": "Invalid request type."})