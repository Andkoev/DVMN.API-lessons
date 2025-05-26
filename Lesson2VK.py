import os
from urllib.parse import urlparse
import requests
from dotenv import load_dotenv


def is_shorten_link(url):
    if not url.startswith('http'):
        url = 'https://' + url.lstrip('/')
    parsed_url = urlparse(url)
    return parsed_url.netloc.lower() == 'vk.cc'


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

    response_data = response.json()
    if 'error' in response_data:
        raise KeyError(response_data['error']['error_msg'])

    return response_data['response']['short_url']


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

    click_stats_data = response.json()
    if 'error' in click_stats_data:
        raise KeyError(click_stats_data['error']['error_msg'])

    return click_stats_data['response']['stats'][0]['views']


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

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err.response.status_code} – {http_err.response.reason}")
    except requests.exceptions.RequestException as req_err:
        print(f"Ошибка сети или запроса: {str(req_err)}")
    except KeyError as key_err:
        print(f"Ошибка в данных: {str(key_err)}")
    except ValueError as val_err:
        print(f"Ошибка значения: {str(val_err)}")
    except Exception as unknown_err:
        print(f"Неизвестная ошибка: {str(unknown_err)}")

    input("\nНажмите Enter, чтобы закрыть...")


if __name__ == '__main__':
    main()
