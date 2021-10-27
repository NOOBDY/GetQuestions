#!/usr/bin/env python
import json
import sys
from typing import Dict

import requests
from bs4 import BeautifulSoup

try:
    with open("login.json", "r") as json_file:
        login_data: Dict[str, str] = json.load(json_file)

    with open("config.txt", "r") as config:
        BASE_URL = f"https://140.124.181.{config.readline()}/upload/"

except FileNotFoundError:
    print("Not yet setup yet")
    exit(1)

if len(sys.argv) == 1:
    print("No question selected")
    exit(1)


with requests.Session() as s:
    s.post(f"{BASE_URL}/Login", login_data, verify=False)
    r = s.get(
        f"{BASE_URL}/showHomework?hwId={int(sys.argv[1]):03}", verify=False)
    soup = BeautifulSoup(r.content.decode("utf-8"), "html5lib")
    res = soup.find(
        "span", style="font-family:標楷體; color:black; behavior:slide; word-wrap:break-word; word-break:normal; font-weight:bold; font-size:medium;")
    if res:
        print(res)
