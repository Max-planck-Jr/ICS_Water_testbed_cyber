import requests

# OpenPLC credentials
PLC_IP = "172.18.0.11"  # Replace with the PLC's IP address
USERNAME = "admin"      # Replace with the OpenPLC web interface username
PASSWORD = "admin"      # Replace with the OpenPLC web interface password

# Login URL and Stop URL
LOGIN_URL = f"http://localhost:8080/login"
STOP_URL = f"http://localhost:8080/stop_plc"

# Session to persist authentication
session = requests.Session()

# Step 1: Login to OpenPLC
login_payload = {
    "username": USERNAME,
    "password": PASSWORD
}
response = session.post(LOGIN_URL, data=login_payload)

if response.status_code == 200 and "Dashboard" in response.text:
    print("Login successful!")

    # Step 2: Send Stop Command
    stop_response = session.get(STOP_URL)
    if stop_response.status_code == 200:
        print("PLC stopped successfully!")
    else:
        print(f"Failed to stop PLC: {stop_response.status_code}")
else:
    print("Failed to log in to OpenPLC!")
