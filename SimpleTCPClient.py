import sys, socket
from scapy.all import sniff, IP, TCP, get_if_hwaddr, Ether, conf
from scapy.layers.http import HTTPRequest
from functools import partial
import subprocess
import time

# Get the MAC address of the default network interface to filter outbound traffic
MY_MAC = get_if_hwaddr(conf.iface).lower()
accessed_internet = False 

accessed_internet = [False] 

def packet_handler(accessed_internet, socket, packet):
    # Ensure the packet has an IP layer and is TCP
    if packet.haslayer(IP) and packet.haslayer(Ether):
            if packet.haslayer(HTTPRequest):
                url = packet[HTTPRequest].Host.decode() + packet[HTTPRequest].Path.decode()
                print(f"OUTBOUND HTTP PACKET {url}")
            elif packet.haslayer(TCP) and packet[TCP].dport == 443: 
                dst_ip = packet[IP].dst
                print(f"HTTPS traffic detected. Destination IP: {dst_ip}")
                message = "cheater!"
                socket.send(message.encode("ascii"))

# The `lfilter` argument allows us to define a Python function to filter packets
# The `prn` argument specifies a function to execute for each packet that passes the filter

def main():
    server = '127.0.0.1'
    port = 48999
    serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSock.connect((server, port))

    sniff(filter="tcp port 80 or tcp port 443", prn=partial(packet_handler, accessed_internet, serverSock), store=0)

    serverSock.close()

main()
