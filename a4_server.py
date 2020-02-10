# Advanced Python for Streaming Analytics
# Fall 2017
# Julian McClellan
 
import socketserver
import numpy as np
from time import sleep

class Handler_TCPServer(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            mu, sigma = 1, 0.1
            s = np.random.normal(mu, sigma, 10)
            for i in s:
                self.request.sendall((str(i) + ' ').encode())
                sleep(1)
        except:
            pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)
    tcp_server.allow_reuse_address = True
    tcp_server.serve_forever()

