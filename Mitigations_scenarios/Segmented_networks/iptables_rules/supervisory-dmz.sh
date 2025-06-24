#!/bin/bash
# router2_firewall.sh

docker exec router_supervisory_dmz sh -c '
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Default policies
iptables -P FORWARD DROP
iptables -P INPUT ACCEPT  
iptables -P OUTPUT ACCEPT

# Allow established connections
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

# DMZ → SUPERVISORY
# Allow HTTP/HTTPS for SCADA web interfaces
iptables -A FORWARD -s 172.18.3.0/24 -d 172.18.2.0/24 -p tcp --dport 80 -j ACCEPT
iptables -A FORWARD -s 172.18.3.0/24 -d 172.18.2.0/24 -p tcp --dport 8080 -j ACCEPT

# SUPERVISORY → DMZ
# Allow database connections (MySQL for ScadaBR)
iptables -A FORWARD -s 172.18.2.0/24 -d 172.18.3.0/24 -p tcp --dport 3306 -j ACCEPT

# Allow responses
iptables -A FORWARD -s 172.18.2.0/24 -d 172.18.3.0/24 -m state --state ESTABLISHED -j ACCEPT

# Block everything else and log
iptables -A FORWARD -j LOG --log-prefix "ROUTER2-BLOCKED: "
iptables -A FORWARD -j DROP

echo "Router 2 firewall configured"
'