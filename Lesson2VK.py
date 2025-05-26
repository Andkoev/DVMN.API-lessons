import os
from urllib.parse import urlparse
import requests
from dotenv import load_dotenv


def is_shorten_link(url):
    if not url.startswith('http'):
        url = 'https://' + url.lstrip('/')
    parsed = urlparse(url)
    return 'vk.cc' in parsed.netloc


def shorten_link(token, url):
    api_url = 'https://api.vk.com/method/utils.getShortLink'
    params = {
        'access_token': token,
        'url': url,
        'private': 0,
        'v': '5.199'
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    data = response.json()
    if 'error' in data:
        raise Exception(data['error']['error_msg'])

    return data['response']['short_url']


def count_clicks(token, short_url):
    key = urlparse(short_url).path.lstrip('/')
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'key': key,
        'v': '5.199'
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    data = response.json()
    if 'error' in data:
        raise Exception(data['error']['error_msg'])

    return data['response']['stats'][0]['views']


def main():
    load_dotenv()
    token = os.getenv('VK_TOKEN')

    if not token:
        print("Ошибка: токен доступа VK не найден.")
        input("\nНажмите Enter, чтобы закрыть...")
        return

    url = input('Введите ссылку: ')

    try:
        if is_shorten_link(url):
            clicks = count_clicks(token, url)
            print("Это короткая ссылка.")
            print("Кол-во переходов по ссылке:", clicks)
        else:
            short_url = shorten_link(token, url)
            print("Это длинная ссылка.")
            print("Сокращенная ссылка:", short_url)

    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка: {e.response.status_code} – {e.response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети или запроса: {str(e)}")
    except Exception as e:
        print(f"Ошибка: {str(e)}")

    input("\nНажмите Enter, чтобы закрыть...")


if __name__ == '__main__':
    main()
