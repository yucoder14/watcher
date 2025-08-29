import sys, socket
from scapy.all import sniff, IP, TCP, get_if_hwaddr, Ether, conf
from functools import partial
import subprocess
import time

# Get the MAC address of the default network interface to filter outbound traffic
MY_MAC = get_if_hwaddr(conf.iface).lower()
accessed_internet = False 

accessed_internet = [False] 

def packet_handler(accessed_internet, socket, packet):
    # Ensure the packet has an IP layer and is TCP
    if not accessed_internet[0]:
        if packet.haslayer(IP) and packet.haslayer(TCP) and packet.haslayer(Ether):
            # Check if the source MAC address is our machine's MAC (outbound)
            if packet[Ether].src.lower() == MY_MAC:
                # Check if the destination port is 443
                if packet[TCP].dport == 443:
                    accessed_internet[0] = True
                    print(f"Outbound HTTPS packet detected!")
                    print(f"Source IP: {packet[IP].src}, Destination IP: {packet[IP].dst}")
                    print("---")
                    time.sleep(5)          
                    command = ["screencapture", "-x", "/tmp/test.png"]
                    message = "cheater!"
                    socket.send(message.encode("ascii"))
                    subprocess.run(command)
                    exit(0)
    else: 
        return
    

# The `lfilter` argument allows us to define a Python function to filter packets
# The `prn` argument specifies a function to execute for each packet that passes the filter

def main():
    server = '127.0.0.1'
    port = 48999
    serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSock.connect((server, port))

    sniff(prn=partial(packet_handler, accessed_internet, serverSock), store=0)

    serverSock.close()

main()
