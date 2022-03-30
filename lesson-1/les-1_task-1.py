import requests

user = 'egortaran'
url = f'https://api.github.com/users/{user}/repos'

response = requests.get(url)
data = response.text

with open('repositories.json', 'w', encoding='utf-8') as file:
    file.write(data)
