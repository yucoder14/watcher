import sys, socket
from enum import Enum
import time
import re
import subprocess

DEFAULT_PORT=48999

class State(Enum): 
    WAIT = 0,
    MONITOR = 1

def check_browsers(): 
    browsers = ["Chrome", "Firefox", "Safari", "Opera"]
        
    found_processes = 0

    for browser in browsers:
        ps_process = subprocess.Popen(["ps", "aux"],stdout=subprocess.PIPE) 
        grep_browser_process = subprocess.Popen(["grep", f"{browser}.app"], 
                                                stdin=ps_process.stdout, stdout=subprocess.PIPE)
        grep_reverse_process_1 = subprocess.Popen(["grep", "-v", "grep"], 
                                              stdin=grep_browser_process.stdout, stdout=subprocess.PIPE)
        grep_reverse_process_2 = subprocess.Popen(["grep", "-v", "Extension"], 
                                                stdin=grep_reverse_process_1.stdout, stdout=subprocess.PIPE)
        wc_process = subprocess.Popen(["wc", "-l"], stdin=grep_reverse_process_2.stdout, stdout=subprocess.PIPE)
        output, error = wc_process.communicate()
        if (int(output.decode().strip()) > 0): return True

    return False

class TesterServer:
    def __init__(self, port=DEFAULT_PORT):
        self.port = port
        self.host = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.state = State.WAIT
        self.proctor_socket = None
        self.proctor_address = None

    def listen_for_proctor(self):
        self.sock.listen(5)

        while True:
            proctor_socket, proctor_address = self.sock.accept()
            while True:
                data = proctor_socket.recv(1024)
                if not len(data):
                    break
                message = data.decode("ascii")
                if (re.match(r"^begin test$" , message)):
                    self.proctor_socket = proctor_socket 
                    self.proctor_address = proctor_address
                    self.state = State.MONITOR
                    return

    def monitor_and_notify(self):
        while self.state == State.MONITOR: 
            try: 
                self.proctor_socket.sendall(f"{check_browsers()}".encode("ascii"))
            except (ConnectionResetError, BrokenPipeError):
                self.state = State.WAIT
                self.proctor_socket.close()

def main():
    # Create a server
    if len(sys.argv) > 1:
        try:
            server = TesterServer(int(sys.argv[1]))
        except ValueError as e:
            print ("Error in specifying port. Creating server on default port.")
            server = TesterServer()
    else:
        server = TesterServer()

    # Listen forever
    while True:
        try: 
            server.listen_for_proctor()
            server.monitor_and_notify()
        except KeyboardInterrupt: 
            break

main()
