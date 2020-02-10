import socket
import statistics
import threading
# from threading import Lock
import numpy as np

host_ip, server_port = "127.0.0.1", 9999

class tcp_client(threading.Thread):
    def __init__(self, offset):
        super().__init__()
        self.offset = offset

    def work_with_server(self):
        global res_mean
        global res_stdev
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_client.connect((host_ip, server_port))
            r_list = []
            while True:
                received = tcp_client.recv(1024)
                if not received:
                    mean = np.mean(r_list)
                    stdev = np.std(r_list)
                    res_mean.append(mean)
                    res_stdev.append(stdev)
                    break
                # store received into a list
                r_list.append(float(received))
        finally:
            tcp_client.close()

    def run(self):
        self.work_with_server()

thread_number = 5
res_mean, res_stdev, thread_list = [], [], []

for i in range(thread_number):
    thread_list.append(tcp_client(i))

for i in range(thread_number):
    thread_list[i].start()

for i in range(thread_number):
    thread_list[i].join()

print("RESULT\n")
print("Mean of all {} means: {}\n".format(len(res_mean), np.mean(res_mean)))
print("Mean of all {} stdevs: {}\n".format(len(res_stdev), np.std(res_stdev)))
