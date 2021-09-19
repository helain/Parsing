import json
import requests

api_url = 'https://api.sallinggroup.com/v2/stores'
token = '54b3d945-0a95-4399-ab0b-135dfca1a2c4'

req = requests.get(f'{api_url}', headers={'Authorization':f'Bearer {token}'})

result = req.json()


with open ('DZ_2.json', 'w') as f:
    json.dump(result, f, indent=4)

