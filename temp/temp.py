import json

with open("data.json", "r") as file:
    data = json.loads(str(file))

print(data)
# print(len(data.keys()))
