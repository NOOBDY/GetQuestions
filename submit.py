#!/usr/bin/env python
import json
import sys
from pprint import pprint
from time import time

import urllib3
from bs4 import BeautifulSoup
from requests import Session
from urllib3.exceptions import InsecureRequestWarning

from utils import login

urllib3.disable_warnings(category=InsecureRequestWarning)


def checkStatus(s: Session, url: str, index: str):
    s.get(f"{url}/upLoadHw?hwId={index}&l=Python")


def delete(s: Session, url: str, index: str):
    s.get(f"{url}/delHw?title={index}")


def submit(s: Session, url: str, index: str, filepath: str):
    try:
        file = open(filepath, "r")
    except FileNotFoundError:
        print("Can't find specified file")
        exit(1)

    filename = f"{json.load(open('login.json'))['name']}_{index}_{round(time() * 1000)}.py"

    r = s.post(f"{url}/upLoadFile", files={"file": file},
               data={"name": "hwFile", "filename": filename})

    pprint(r.request.body)

    pprint(r.json())


if __name__ == "__main__":
    with Session() as s:
        url, index = login(s)
        submit(s, url, index, sys.argv[2])
