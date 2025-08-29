import sys, socket
import time


def init_connection(server, port):
    # create a TCP/IP socket using ipv4
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.connect((server, port))
    
    return server_socket

def send_messages(sockets, message):
    for socket in sockets:
        socket.send(message.encode("ascii"))

def close_connection(sockets):
    for socket in sockets:
        socket.close()

def main():
    servers = [
        '127.0.0.1',
        '127.0.0.1',
        '127.0.0.1',
        '127.0.0.1',
        '127.0.0.1',
    ]
    #    servers = [ 
    #        'olin310-01.mathcs.carleton.edu',
    #        'olin310-02.mathcs.carleton.edu',
    #        'olin310-03.mathcs.carleton.edu',
    #        'olin310-04.mathcs.carleton.edu',
    #        'olin310-05.mathcs.carleton.edu',
    #        'olin310-06.mathcs.carleton.edu'
    #    ]
    ports =[ 48999, 49000, 49001, 49002, 49003 ]
    server_sockets = list(map(init_connection, servers, ports))
    message = "begin test"
    while True: 
        send_messages(server_sockets, message)
        time.sleep(1)
        
    close_connection(server_sockets)


main()
