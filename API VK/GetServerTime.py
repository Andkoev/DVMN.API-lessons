import os
import requests
from dotenv import load_dotenv

API_BASE ="https://api.vk.com/method"
API_VERSION ="5.199"

load_dotenv()
auth_key=os.getenv("VK_TOKEN")

def get_server_time(token: str) -> str:
    response = requests.get(
    f"{API_BASE}/utils.getServerTime",
    params = {"access_token": token, "v":API_VERSION},
)
    return response.text

if __name__ == "__main__":
    print(get_server_time(auth_key))