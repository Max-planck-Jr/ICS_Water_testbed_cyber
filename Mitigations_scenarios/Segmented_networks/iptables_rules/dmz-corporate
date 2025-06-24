#!/bin/bash  
# router3_firewall.sh

docker exec router_dmz_corporate sh -c '
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Default policies
iptables -P FORWARD DROP
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT

# Allow established connections
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

# CORPORATE → DMZ
# Allow SSH for administration (restricted times/sources)
iptables -A FORWARD -s 172.18.4.0/24 -d 172.18.3.0/24 -p tcp --dport 22 -j ACCEPT

# Allow HTTPS for web management
iptables -A FORWARD -s 172.18.4.0/24 -d 172.18.3.0/24 -p tcp --dport 443 -j ACCEPT

# DMZ → CORPORATE
# Block all initiated connections from DMZ to corporate
iptables -A FORWARD -s 172.18.3.0/24 -d 172.18.4.0/24 -j LOG --log-prefix "DMZ-TO-CORP-BLOCKED: "
iptables -A FORWARD -s 172.18.3.0/24 -d 172.18.4.0/24 -j DROP

# Block everything else and log
iptables -A FORWARD -j LOG --log-prefix "ROUTER3-BLOCKED: "
iptables -A FORWARD -j DROP

echo "Router 3 firewall configured"
'