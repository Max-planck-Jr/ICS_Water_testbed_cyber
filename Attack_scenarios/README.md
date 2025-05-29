# ICS Water Testbed - Tools Installation Guide
This README provides installation instructions for all basic tools used in the Industrial Control Systems (ICS) cybersecurity testbed research. Complex tools are documented in their respective scenarios

## *NB:*
Most of these tools would be found in the Dockerfile of corresponding components, nevertheless, the testbed's flexibility enables you to install any tool you wish

## *Installing virtual environment* 
Some python librairies must be installed in virtual env.

Run: 
```
# Install venv
python3 -m venv ics-env
# Activate created ics-env
source ics-env/bin/activate
```

## *Installing network tools* 
Network tools used for scanning and penetration testing in the ICS testbed, you might install them in the attacker's machine, the choice is yours. Since we are using docker, there's no need for sudo. The testbed is really flexible so you could any other tool of your choice. 

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
# Install network discover for scanning
apt install netdiscover
apt install -y curl
```

## *Installing network and web pentesting tools* 
Some tools were used to infiltrate the network 

Run: 
```
# Install netcat for network pentesting
apt install netcat-traditional
# Install arpspoof for arp spoofing attacks
apt install -y dsniff
# Install whatweb for Web application fingerprinting tool
apt install whatweb -y
# Install nikto for Web vulnerability scanner
apt install nikto -y
# Install medusa for Fast, parallel password brute-forcing tool
apt install -y medusa
```

## *Some usage examples*
Here, we show some usage examples, but more details are found in respective scenarios

Run this to scan the Scada networks
```
# Network discovery
nmap -sn target_network_ip
# Modbus port scan
nmap -p 502 target-ip  
# Network scan
arp-scan --interface=eth0 172.18.0.0/24
```

Run this to spoof two targets (Example plc and scadaBR)
```
# Example spoofing plc11 and scadaBR
arpspoof -i eth0 -t plc_ip scadaBR_ip
arpspoof -i eth0 -t scadaBR_ip plc_ip 
```

Run this to capture traffic between targets
```
# Capture any modbus traffic generating a pcap file afterward
tcpdump -i eth0 -w capture.pcap port 502
# Caputre traffic going towards a target
tcpdump -i eth0 dst target_ip
```

Run this to exploit some web vulnerabilities (Example scadaBR)
```
# Recall scadaBR is exposed to 8080 when its container is launched
whatweb http://scadaBR-ip:8080
nikto -h http://target-ip:8080
# Brute force attacks on target ip
medusa -h target-ip -u admin -P passwords.txt -M http
```

## Some attacking scripts developped by Matrix
Matrix written by Karl contains several attack scripts used to exploit modbus vulnerabilites. Don't hesitate to get to his git hub repository for more details.

bash
```
# Clone the repository
git clone https://github.com/SpiderLabs/MATRIX.git
cd MATRIX
```

