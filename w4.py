import json

order = {'price': 12, 'volume': 100}
a = json.dumps(order)

print(json.dumps(order, sort_keys=True, indent=4, separators=(',', ': ')))
