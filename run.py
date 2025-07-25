import subprocess
import sys

# List of microservices to launch in the background
microservices = [
    "add_card.py",
    "edit_card.py",
    "move_card.py",
    "load_set.py",
    "delete_card.py",
    "save_set.py"
]

# Store subprocesses
processes = []

try:
    # Start microservices in the background
    for script in microservices:
        print(f"Launching {script}...")
        p = subprocess.Popen([sys.executable, script])
        processes.append(p)

    # Start UI in the foreground (blocking)
    print("Launching UI...")
    subprocess.call([sys.executable, "ui.py"])

except KeyboardInterrupt:
    print("\nInterrupted. Cleaning up...")

finally:
    # Terminate all background microservices
    print("Shutting down microservices...")
    for p in processes:
        p.terminate()
