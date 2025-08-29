import sys, socket
DEFAULT_PORT=48999

class TCPServer:
    def __init__(self, port=DEFAULT_PORT):
        self.port = port
        self.host = "localhost"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)

        while True:
            proctorSock, proctorAddr = self.sock.accept()
            print ("Connection received from ",  proctorSock.getpeername())
            # Get the message and echo it back
            while True:
                data = proctorSock.recv(1024)
                if not len(data):
                    break
                print ("Received message:  " + data.decode("ascii"))
                proctorSock.sendall(data)
            proctorSock.close()

def main():
    # Create a server
    if len(sys.argv) > 1:
        try:
            server = TCPServer(int(sys.argv[1]))
        except ValueError as e:
            print ("Error in specifying port. Creating server on default port.")
            server = TCPServer()
    else:
        server = TCPServer()

    # Listen forever
    print ("Listening on port " + str(server.port))
    server.listen()

main()
