import sys, socket
from enum import Enum
DEFAULT_PORT=48999

class State(Enum): 
    WAIT = 0,
    MONITOR = 1

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
            print ("Connection received from ",  proctor_socket.getpeername())
            # Get the message and echo it back
            while True:
                data = proctor_socket.recv(1024)
                if not len(data):
                    break
                print ("Received message:  " + data.decode("ascii"))
                if (data.decode("ascii") == "begin test"):
                    self.state = State.MONITOR
                    self.proctor_socket = proctor_socket
                    self.proctor_address = proctor_address
                    return

    def monitor(self):
        dummy = "bobobo"
        self.proctor_socket.send(dummy.encode("ascii"))


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
    server.listen_for_proctor()
    print(server.state)
    server.monitor()

main()
