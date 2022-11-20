"""Getting information from webpage."""

from typing import Any, Dict, Optional

import requests
import json

import logging

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def request_via_proxy(
    target_url: str, proxy_ip: Optional[str], port: Optional[str]
) -> Dict[str, Any]:
    res = {}
    proxies = (
        {"http": f"http://{proxy_ip}:{port}"} if all([proxy_ip, port]) else None
    )
    response = requests.get(target_url, proxies=proxies)
    if not str(response.status_code).startswith("2"):
        logging.info(
            "Got invalid response (%s): %s", response.status_code, response.text
        )
    else:
        res = response.json()
    return res


def prettify_json(ugly_json: str, indent: int = 4):
    parsed = json.loads(ugly_json)
    return json.dumps(parsed, indent=indent)
