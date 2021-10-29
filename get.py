#!/usr/bin/env python
from requests import Session
from bs4 import BeautifulSoup

from utils import login
import html

def get(s: Session, url: str, index: str) -> None:
    r = s.get(f"{url}/showHomework?hwId={index}", verify=False)

    soup = BeautifulSoup(r.content.decode("utf-8"), "html5lib")
    res = soup.find(
        "span", style="font-family:標楷體; color:black; behavior:slide; word-wrap:break-word; word-break:normal; font-weight:bold; font-size:medium;")

    print(index)
    if res:
        for line in str(res).split("<br/>")[1:-1]:
            print(html.unescape(line.strip()))

if __name__ == "__main__":
    with Session() as s:
        url, index = login(s)
        get(s, url, index)
