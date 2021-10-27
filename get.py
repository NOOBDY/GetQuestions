from typing import Dict
import requests
import json
from bs4 import BeautifulSoup

with open("login.json", "r") as json_file:
    login_data: Dict[str, str] = json.load(json_file)

with requests.Session() as s:
    s.post("https://140.124.181.36/upload/Login", login_data, verify=False)
    r = s.get("https://140.124.181.36/upload/showHomework?hwId=007", verify=False)
    soup = BeautifulSoup(r.content.decode("utf-8"), "html5lib")
    res = soup.find(
        "span", style="font-family:標楷體; color:black; behavior:slide; word-wrap:break-word; word-break:normal; font-weight:bold; font-size:medium;")
    if res:
        print(res)
