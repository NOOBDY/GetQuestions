#!/usr/bin/env python
from requests import Session
from bs4 import BeautifulSoup
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from utils import login

urllib3.disable_warnings(category=InsecureRequestWarning)


def delete(s: Session, url: str, index: str):
    s.get(f"{url}/delHw?title={index}")


if __name__ == "__main__":
    with Session() as s:
        url, index = login(s)
        delete(s, url, index)
