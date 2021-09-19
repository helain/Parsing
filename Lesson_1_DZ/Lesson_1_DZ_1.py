import json
import requests

url = 'https://api.github.com/'
user = 'helain'

req = requests.get(f'{url}users/{user}/repos')

resp = req.json()

for i in range(len(resp)):
    names_only.append(resp[i]['name'])

with open ('DZ_1_full.json', 'w') as f:
    json.dump(resp, f, indent=4)

with open ('DZ_1_names_only.txt', 'w') as f:
    for i in range(len(resp)):
        f.write(resp[i]['name'] + '\n')

