#!/usr/bin/env python
from requests import Session
from bs4 import BeautifulSoup

from utils import login


def get(s: Session, base_url: str, index: str) -> None:
    r = s.get(f"{base_url}/showHomework?hwId={index}", verify=False)

    soup = BeautifulSoup(r.content.decode("utf-8"), "html5lib")
    res = soup.find(
        "span", style="font-family:標楷體; color:black; behavior:slide; word-wrap:break-word; word-break:normal; font-weight:bold; font-size:medium;")

    if res:
        for line in res.text.strip().split("\n"):
            print(line.strip())


if __name__ == "__main__":
    with Session() as s:
        base_url, index = login(s)
        get(s, base_url, index)
