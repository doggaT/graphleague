import requests


def rate_limit_exceeded(exception):
    if isinstance(exception, requests.exceptions.HTTPError):
        if exception.response.status_code == 429:
            return True
    return False
