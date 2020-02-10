import urllib.request

with urllib.request.urlopen('http://127.0.0.1:5000/hello') as f:
    print(f.read(300)) 

import urllib.request
import json
newConditions = {"con1":40, "con2":20, "con3":99, "con4":40,
        "password":"1234"}
params = json.dumps(newConditions).encode('utf8')

req = urllib.request.Request('http://localhost:5000/messages', data=params, headers={'content-type': 'application/json'})

response = urllib.request.urlopen(req)

print(response.read().decode('utf8'))
