import requests as req
import json


API_KEY='''88e45ac1-6083-478d-bac0-6523f4bc4c76'''

phnom_penh_aq=json.dumps(req.get(f"http://api.airvisual.com/v2/city?city=Phnom Penh&state=Phnom Penh&country=Cambodia&key={API_KEY}").json(), indent=4)

print(phnom_penh_aq)

print(json.loads(phnom_penh_aq)["data"]["current"]["pollution"]["aqius"])

