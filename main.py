import requests
from urllib.parse import quote

template = 'https://wttr.in/{}'
cities = ['Шереметьево', 'Череповец', 'Лондон']

flags = ['mM','nTq']
params = '&'.join(flags) + '&lang=ru'

for city in cities:
    encoded_city = quote(city)
    url = f'{template.format(encoded_city)}?{params}'
    response = requests.get(url)
    response.raise_for_status()
    print(response.text)

input()
