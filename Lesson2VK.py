import os
from urllib.parse import urlparse
import requests
from dotenv import load_dotenv

API_URL = "https://api.vk.com/method"
API_VERSION = "5.199"


def ensure_vk_ok(response_dict):
    if "error" in response_dict:
        message = response_dict["error"].get("error_msg", "VK API error")
        raise KeyError(message)
    return response_dict["response"]


def is_shorten_link(token: str, url: str) -> bool:
    parsed = urlparse(url.strip())
    key = parsed.path.lstrip("/") if parsed.netloc.lower() == "vk.cc" else ""
    if not key:
        return False
    resp = requests.get(
        f"{API_URL}/utils.getLinkStats",
        params={"access_token": token, "key": key, "v": API_VERSION},
    )
    resp.raise_for_status()
    return "error" not in resp.json()


def shorten_link(token: str, url: str) -> str:
    resp = requests.get(
        f"{API_URL}/utils.getShortLink",
        params={"access_token": token, "url": url, "private": 0, "v": API_VERSION},
    )
    resp.raise_for_status()
    vk_response = ensure_vk_ok(resp.json())
    return vk_response["short_url"]


def count_clicks(token: str, short_url: str) -> int:
    key = urlparse(short_url).path.lstrip("/")
    resp = requests.get(
        f"{API_URL}/utils.getLinkStats",
        params={"access_token": token, "key": key, "v": API_VERSION},
    )
    resp.raise_for_status()
    vk_response = ensure_vk_ok(resp.json())
    stats_list = vk_response.get("stats", [])
    return stats_list[0]["views"] if stats_list else 0


def main():
    load_dotenv()
    token = os.getenv("VK_TOKEN")
    if not token:
        print("Ошибка: переменная окружения VK_TOKEN не найдена.")
        return
    user_url = input("Вставьте ссылку: ").strip()
    try:
        if is_shorten_link(token, user_url):
            clicks = count_clicks(token, user_url)
            print(f"Это короткая ссылка. Переходов: {clicks}")
        else:
            short_url = shorten_link(token, user_url)
            print(f"Это длинная ссылка. Сокращённая: {short_url}")
    except requests.exceptions.HTTPError as http_err:
        code = getattr(http_err.response, "status_code", "?")
        reason = getattr(http_err.response, "reason", "")
        print(f"HTTP ошибка: {code} — {reason}")
    except requests.exceptions.RequestException as req_err:
        print(f"Ошибка сети/запроса: {req_err}")
    except KeyError as vk_err:
        print(f"Ошибка VK API: {vk_err}")


if __name__ == "__main__":
    main()
