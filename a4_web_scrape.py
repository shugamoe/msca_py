import socket
import pdb
from nltk.tokenize import RegexpTokenizer

# request = b"GET / HTTPS/1.1\nHost: stackoverflow.com\n\n"
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(("stackoverflow.com", 80))
# s.send(request)
# 
# while True:
#     result = s.recv(512)
#     if (len(result) < 1):
#         break
#     pdb.set_trace()


import urllib.request
from bs4 import BeautifulSoup

with urllib.request.urlopen("http://www.stackoverflow.com") as url:
    s = url.read()
    soup = BeautifulSoup(s, "lxml")
    print("There are {} hyperlinks on this webpage".format(len(soup.find_all("a"))))
    tokenizer = RegexpTokenizer(r'\w+')
    print("There are {} alphanumeric words on this webpage".format(
        len(tokenizer.tokenize(soup.text))))
