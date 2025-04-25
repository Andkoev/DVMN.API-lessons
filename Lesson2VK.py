import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('VK_TOKEN')


def is_shorten_link(url):
    if not url.startswith('http'):
        url = 'https://' + url.lstrip('/')
    parsed = urlparse(url)
    return 'vk.cc' in parsed.netloc


def shorten_link(url):
    api_url = 'https://api.vk.com/method/utils.getShortLink'
    params = {
        'access_token': TOKEN,
        'url': url,
        'private': 0,
        'v': '5.199'
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    if 'error' in data:
        return f"Ошибка: {data['error']['error_msg']}"

    return data['response']['short_url']


def count_clicks(short_url):
    key = short_url.split('/')[-1]
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    params = {
        'access_token': TOKEN,
        'key': key,
        'v': '5.199'
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    if 'error' in data:
        return f"Ошибка: {data['error']['error_msg']}"

    return data['response']['stats'][0]['views']


def main():
    if not TOKEN:
        print("Ошибка: токен доступа VK не найден.")
        input("\nНажмите Enter, чтобы закрыть...")
        return

    input_url = input('Введите ссылку: ')

    if is_shorten_link(input_url):
        clicks = count_clicks(input_url)
        if isinstance(clicks, str) and clicks.startswith("Ошибка"):
            print(clicks)
        else:
            print("Это короткая ссылка.")
            print("Кол-во переходов по ссылке:", clicks)
    else:
        short_url = shorten_link(input_url)
        if isinstance(short_url, str) and short_url.startswith("Ошибка"):
            print(short_url)
        else:
            print("Это длинная ссылка.")
            print("Сокращенная ссылка:", short_url)

    input("\nНажмите Enter, чтобы закрыть...")


if __name__ == '__main__':
    main()