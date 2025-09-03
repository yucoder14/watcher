import sys, socket
from datetime import datetime
from host import Host, HostStatus

class ProctorServer: 
    def __init__(self, hosts):
        self.tester_sockets = [self.init_connection(host.get_hostname(), host.get_port()) for host in hosts]
        self.hosts = hosts

    def init_connection(self, server, port):
        # create a TCP/IP socket using ipv4
        try: 
            server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server_socket.connect((server, port))
        except (ConnectionRefusedError, socket.gaierror):
            server_socket = None 
            pass 
        
        return server_socket

    def query_testers(self): 
        replies = []
        for i in range(len(self.tester_sockets)): 
            socket = self.tester_sockets[i] 
            host = self.hosts[i] 
            if socket is not None: 
                response = socket.recv(1024).decode("ascii") 
                if (len(response)):
                    replies.append(response)
                else:
                    replies.append("Offline")
                    self.tester_sockets[i] = None
            else: 
                replies.append("Offline")
                self.tester_sockets[i] = self.init_connection(host.get_hostname(), host.get_port())
                if self.tester_sockets[i] is not None: 
                    self.tester_sockets[i].send("begin test".encode("ascii"))
        return replies
        

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
            if socket is not None: 
                socket.send(message.encode("ascii"))

    def close_connection(self):
        for socket in self.tester_sockets:
            socket.close()
