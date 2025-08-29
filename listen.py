from scapy.all import sniff, IP, TCP, get_if_hwaddr, Ether, conf
from functools import partial
import subprocess
import time

# Get the MAC address of the default network interface to filter outbound traffic
MY_MAC = get_if_hwaddr(conf.iface).lower()
connection = False 

connection = [False] 

def packet_handler(connection, packet):
    # Ensure the packet has an IP layer and is TCP
    if not connection[0]:
        if packet.haslayer(IP) and packet.haslayer(TCP) and packet.haslayer(Ether):
            # Check if the source MAC address is our machine's MAC (outbound)
            if packet[Ether].src.lower() == MY_MAC:
                # Check if the destination port is 443
                if packet[TCP].dport == 443:
                    connection[0] = True
                    print(f"Outbound HTTPS packet detected!")
                    print(f"Source IP: {packet[IP].src}, Destination IP: {packet[IP].dst}")
                    print("---")
                    command = ["screencapture", "-x", "/tmp/test.png"]
                    subprocess.run(command)
                    time.sleep(5)          
                    exit(0)
    else: 
        return
    
print("Starting outbound port 443 packet capture. Press Ctrl+C to stop.")

# The `lfilter` argument allows us to define a Python function to filter packets
# The `prn` argument specifies a function to execute for each packet that passes the filter
sniff(prn=partial(packet_handler, connection), store=0)
