import sys, socket
import time

class ProctorServer: 
    def __init__(self, tester_servers, tester_ports):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tester_sockets = list(map(self.init_connection, tester_servers, tester_ports))

    def init_connection(self, server, port):
        # create a TCP/IP socket using ipv4
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.connect((server, port))
        
        return server_socket

    # i think i might need different proctor socket for each tester socket?
    def lisent_to_testers(self): 
        while True: 
            try: 
                from_testers = [socket.recv(1024) for socket in self.tester_sockets]
                returns = [True for returned in from_testers if eval(returned.decode("ascii"))]
                violations = list(map(lambda violation, socket: socket.getsockname()[0] if violation else None, returns, self.tester_sockets))

                if len(violations):
                    print(violations)
            # or some other mechanism to signal the end
            except KeyboardInterrupt: 
                self.close_connection()
                break

    def send_messages(self, message):
        for socket in self.tester_sockets:
            socket.send(message.encode("ascii"))

    def close_connection(self):
        for socket in self.tester_sockets:
            socket.close()

def main():
    tester_servers = [
        "localhost",
        "localhost",
        "localhost",
        "localhost",
        "localhost"
    ]
#    ports = [49001]
    ports = [49000, 49001, 49002, 49003, 49004]
    server = ProctorServer(tester_servers, ports)
    server.send_messages("begin test")
    server.lisent_to_testers()

#    server.close_connection()

main()
