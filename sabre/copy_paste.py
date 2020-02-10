import requests
import base64
client_id=b"V1:99276b8l9reqsssl:DEVCENTER:EXT"
client_secret=b"eEJF29wm"

client_id64=base64.b64encode(client_id)
client_secret64=base64.b64encode(client_secret)

credentials_part = client_id64.decode("utf-8") + ":" + client_secret64.decode("utf-8")
credentials = base64.b64encode(credentials_part.encode("utf-8"))

url = "https://api.test.sabre.com/v2/auth/token"
headers = {"Authorization": "Basic " + credentials.decode("utf-8")}
params = {"grant_type": "client_credentials"}

r = requests.post(url, headers=headers, data=params)
assert r.status_code is 200, "Oops..."
token = r.json()
