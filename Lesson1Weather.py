import requests
from urllib.parse import quote

template = 'https://wttr.in/{}'
cities = ['Шереметьево', 'Череповец', 'Лондон']
params = {'nTq': '', 'mM': '', 'lang': 'ru'}

for city in cities:
    url = template.format(quote(city))
    response = requests.get(url, params=params)
    response.raise_for_status()
    print(response.text)