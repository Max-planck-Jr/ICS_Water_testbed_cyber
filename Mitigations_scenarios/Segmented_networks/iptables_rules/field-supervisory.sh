#!/bin/bash
# router1_firewall.sh

docker exec router_field_supervisory sh -c '
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Default policies
iptables -P FORWARD DROP
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT

# Allow established connections
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

# SUPERVISORY → FIELD DEVICE
# Allow Modbus/TCP (502) from supervisory to field devices
iptables -A FORWARD -s 172.18.2.0/24 -d 172.18.1.0/24 -p tcp --dport 502 -j ACCEPT

# Allow HTTP for OpenPLC web interface (restricted)
iptables -A FORWARD -s 172.18.2.0/24 -d 172.18.1.0/24 -p tcp --dport 8080 -j ACCEPT

# FIELD DEVICE → SUPERVISORY  
# Allow responses only (no initiated connections from field)
iptables -A FORWARD -s 172.18.1.0/24 -d 172.18.2.0/24 -m state --state ESTABLISHED -j ACCEPT

# Block everything else and log
iptables -A FORWARD -j LOG --log-prefix "ROUTER1-BLOCKED: "
iptables -A FORWARD -j DROP

echo "Router 1 firewall configured"
'