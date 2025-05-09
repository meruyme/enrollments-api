from typing import Union

import requests


def external_get_request(
    url: str, username: str, password: str, params: dict = None
) -> Union[dict, list]:
    response = requests.get(
        url,
        params=params,
        auth=(username, password),
    )
    response.raise_for_status()
    body = response.json()

    return body
