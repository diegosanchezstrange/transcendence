import requests
from requests import Response
from requests.exceptions import RequestException


def request_intra(url: str, headers: dict, max_attempts=5) -> Response:
    attempts = 0
    while attempts < max_attempts:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200 or response.status_code == 401:
                return response
            else:
                print(f"Attempt {attempts + 1} failed: Status code {response.status_code}")
        except RequestException as e:
            print(f"An exception occurred: {e}")
            break
        finally:
            attempts += 1

    raise RequestException("Could not connect to intra.")
