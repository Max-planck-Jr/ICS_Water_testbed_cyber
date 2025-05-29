# ICS Water Testbed - Tools Installation Guide
This README provides installation instructions for all basic tools used in the Industrial Control Systems (ICS) cybersecurity testbed research. Complex tools are documented in their respective folders

## *Installing virtual environment* 
Some python librairies must be installed in virtual env.

Run: 
```
# Install venv
python3 -m venv ics-env
# Activate created ics-env
source ics-env/bin/activate
```

### *Installing network tools* 
Network tools used for scanning and penetration testing in the ICS testbed

Run:
```
$ Install iputils-ping important for network test
install -y iputils-ping
# Install iproute for ip config
apt install iproute2 -y 
# Install tcpdump to capture traffic
apt install -y tcpdump
# Install wireshark to analyze traffic
apt install -y wireshark
usermod -aG wireshark $USER
# Install nmap for network scanning
apt install nmap
# Install arp-scan for network discoveries
apt install arp-scan
# Install telnet to test connectivity
apt install -y telnet
# Install nikto 
apt install nikto -y
# Install whatweb
apt install whatweb -y
# Install network discover for scanning
apt install netdiscover
# Install netcat for network pentesting
apt install netcat-traditional
```