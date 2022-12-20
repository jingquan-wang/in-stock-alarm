"""Getting information from webpage."""

from typing import Optional, List

import requests
import json

import logging

import re

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def request_via_proxy(
    target_url: str, proxy_ip: Optional[str] = None, port: Optional[str] = None
) -> str:
    res = ""
    proxies = (
        {"http": f"http://{proxy_ip}:{port}"} if all([proxy_ip, port]) else None
    )
    response = requests.get(target_url, proxies=proxies)
    logging.info(
        "Getting response from %s; proxy: %s:%s", target_url, proxy_ip, port
    )
    if not str(response.status_code).startswith("2"):
        logging.info(
            "Got invalid response (%s): %s",
            response.status_code,
            response.text,
        )
    else:
        res = response.text
    return res


def prettify_json(ugly_json: str, indent: int = 4):
    parsed = json.loads(ugly_json)
    return json.dumps(parsed, indent=indent)


def search_elements(webpage_content: str, regex_pattern: str) -> List[str]:
    return set(re.findall(webpage_content, regex_pattern))
