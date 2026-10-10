
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("MONITOR_URL", "https://example.com")
CHECK_INTERVAL = 30
was_down = False


def check_server():
    try:
        response = requests.get(URL, timeout=5)

        if response.status_code >= 500:
            return False, f"HTTP {response.status_code}"

        return response.status_code < 400, (
            f"HTTP {response.status_code}"
        )

    except requests.RequestException as error:
        return False, str(error)


def send_sms(message):
    # Connect your SMS provider here.
    # Do not put API credentials directly in this function.
    print(f"SMS alert to send: {message}")


while True:
    is_up, details = check_server()

    print(f"{URL}: {details}")

    if not is_up and not was_down:
        send_sms(f"Alert: {URL} may be down! {details}")

    was_down = not is_up
    time.sleep(CHECK_INTERVAL)
