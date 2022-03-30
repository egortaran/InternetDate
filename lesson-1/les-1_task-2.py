import json
import requests

method = 'groups.get'
access_token = 'секрет :) '
extended = 1  # All info
version = '5.131'

url = f'https://api.vk.com/method/{method}?access_token={access_token}&extended={extended}&v={version}'
response = requests.get(url)

data = json.loads(response.text)

with open('groups.txt', 'w', encoding='utf-8') as file:
    for item in data['response']['items']:
        file.write(item['name'] + '\n')
