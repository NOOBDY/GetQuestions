#!/usr/bin/env python
import json
import sys
from time import time

import urllib3
from bs4 import BeautifulSoup
from requests import Session
from urllib3.exceptions import InsecureRequestWarning

from utils import login

urllib3.disable_warnings(category=InsecureRequestWarning)


def checkStatus(s: Session, base_url: str, index: str) -> str:
    url = f"{base_url}/upLoadHw?hwId={index}&l=Python"
    s.get(url)

    return url


def delete(s: Session, url: str, index: str):
    s.get(f"{url}/delHw?title={index}")


def submit(s: Session, base_url: str, index: str, filepath: str):
    try:
        file = open(filepath, "r")

    except FileNotFoundError:
        print("Can't find specified file")
        exit(1)

    filename = f"{json.load(open('login.json'))['name']}_{index}_{round(time() * 1000)}.py"

    url = checkStatus(s, base_url, index)

    s.headers.update({"Referer": url})
    s.headers.update({"X-Requested-With": "XMLHttpRequest"})

    r = s.post(f"{base_url}/upLoadFile",
               files={"hwFile": (filename, file, "text/x-python")})

    if r.json()["success"]:
        print("Upload success")


if __name__ == "__main__":
    with Session() as s:
        base_url, index = login(s)
        delete(s, base_url, index)
        submit(s, base_url, index, sys.argv[2])
