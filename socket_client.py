# Socket Clinet from w3

import socket
import sys

HOST = 'localhost'
PORT = 9999

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    data = "wtf is happening rn"
    data = data.encode()
    sock.sendall(data)

    # Receive data from the server and shutdown
    received = sock.recv(1024)
finally:
    sock.close()

print("Sent:    {}".format(data))
print("Received:    {}".format(received))

