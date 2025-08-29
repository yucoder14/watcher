import sys, socket
from enum import Enum
import time
import re

DEFAULT_PORT=48999

class State(Enum): 
    WAIT = 0,
    MONITOR = 1

class TesterServer:
    def __init__(self, port=DEFAULT_PORT):
        self.port = port
        self.host = "localhost"
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
                print ("Received message:  " + data.decode("ascii"))
                message = data.decode("ascii")
                if (re.match(r"^begin test$" , message)):
                    self.state = State.MONITOR
                    self.proctor_socket = proctor_socket 
                    self.proctor_address = proctor_address
                    return

    def monitor_and_notify(self):
        while self.state == State.MONITOR: 
            dummy = f"hello from {self.host}:{self.port}\n"
            try: 
                time.sleep(1)
                self.proctor_socket.sendall(dummy.encode("ascii"))
            except ConnectionResetError:
                self.state = State.WAIT
            except BrokenPipeError: 
                self.state = State.WAIT

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
    print ("Listening on port " + str(server.port))
    while True:
        print(server.state)
        server.listen_for_proctor()
        print(server.state)
        server.monitor_and_notify()
        print("connection closed, ending test state")

main()
