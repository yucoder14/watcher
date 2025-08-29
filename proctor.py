import sys, socket
from datetime import datetime

class ProctorServer: 
    def __init__(self, tester_servers, tester_ports):
        self.tester_sockets = list(map(self.init_connection, tester_servers, tester_ports))

    def init_connection(self, server, port):
        # create a TCP/IP socket using ipv4
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.connect((server, port))
        
        return server_socket

    def lisent_to_testers(self): 
        while True: 
            try: 
                from_testers = [tester_socket.recv(1024) for tester_socket in self.tester_sockets]
                returns = [returned.decode("ascii") for returned in from_testers]
                violations = list(map(lambda violation, socket: 
                                        socket.getsockname()[0] if violation == "True" else None, 
                                      returns, self.tester_sockets))

                if len(violations):
                    print(datetime.now(), violations)
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

    ports = [49000, 49001, 49002, 49003, 49004]
    server = ProctorServer(tester_servers, ports)
    server.send_messages("begin test")
    server.lisent_to_testers()

main()
