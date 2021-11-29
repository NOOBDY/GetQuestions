import json
import sys
from sys import exit  # i need to import exit or the binary will complain
from time import time
from typing import Dict, List, Tuple

import urllib3
from bs4 import BeautifulSoup
from bs4.element import Tag
from dateutil import parser
from requests import Session
from requests.exceptions import ConnectTimeout, SSLError
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)


def _get_test_status(self, id_: int, index: str) -> Dict[str, bool]:
    session = self.session
    base_url = self.base_url

    # you can check other people's upload status while logged in lol
    res = session.get(
        f"{base_url}/CheckResult?questionID={index}&studentID={id_}")

    soup = BeautifulSoup(res.content.decode(), "html5lib")
    res: List[Tag] = list(soup.find_all("tr"))[1:]

    cases = {}
    for test in res:
        case, status = [i.get_text().strip() for i in test.find_all("td")]
        cases[case] = status != '測試失敗'

    return cases


if __name__ == "__main__":
    print("Don't execute this file directly")
    exit(0)
