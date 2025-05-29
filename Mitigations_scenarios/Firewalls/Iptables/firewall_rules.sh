#!/bin/bash
# firewall-rules.sh

# Clear existing rules
iptables -F
iptables -X

# Set default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Add your rules here
# Clear existing rules
iptables -F
iptables -X

# Set default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow specific SCADA BR to PLC communication (example IPs)
iptables -A INPUT -p tcp --dport 502 -s 172.18.0.9 -d 172.18.0.11 -j ACCEPT  # SCADA BR to PLC
iptables -A INPUT -p tcp --sport 502 -s 172.18.0.11 -d 172.18.0.9 -j ACCEPT  # PLC response back

# Drop all other attempts to access SCADA/PLC ports
iptables -A INPUT -p tcp --dport 502 -j DROP

# Block scanning attempts
iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
iptables -A INPUT -p tcp --tcp-flags ALL FIN,URG,PSH -j DROP
iptables -A INPUT -p tcp --tcp-flags ALL SYN,RST,ACK,FIN,URG -j DROP

# Save rules
iptables-save > /etc/iptables/rules.v4