import json
import os
import json


if os.path.exists("./keys.json"):
    with open("./keys.json", "r") as file:
        keys = json.load(file)
    if "aqius_prior" in keys:
        print(type(keys["aqius_prior"]))
    else:
        print("Key 'aqius_prior' not found in keys.json")
else:
    print("File 'keys.json' does not exist")