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
    def listen_for_tester(self): 
        while True: 
            try: 
                from_testers = [socket.recv(1024) for socket in self.tester_sockets]
                returns = [returned.decode("ascii") for returned in from_testers if len(returned)]

                if len(returns):
                    print(returns)
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
    ports = [49001, 49002, 49003, 49004, 49005]
    server = ProctorServer(tester_servers, ports)
    server.send_messages("begin test")
    server.listen_for_tester()

#    server.close_connection()

main()
