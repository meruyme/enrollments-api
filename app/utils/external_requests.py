import time
from random import random
from typing import Union

import requests


def external_get_request(
    url: str, username: str, password: str, params: dict = None,
    timeout: int = 10, sleep: float = 0.5, timeout_retries: int = 2,
) -> Union[dict, list]:
    try:
        response = requests.get(
            url,
            params=params,
            auth=(username, password),
            timeout=timeout,
        )
        response.raise_for_status()
        body = response.json()

        return body
    except Exception as e:
        if timeout_retries == 0:
            raise e

        time.sleep(sleep)
        return external_get_request(
            url=url,
            username=username,
            password=password,
            params=params,
            timeout=timeout,
            sleep=sleep + random(),
            timeout_retries=timeout_retries - 1,
        )
