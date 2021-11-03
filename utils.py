import json
import sys
from typing import Dict, Tuple

import urllib3
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from requests import Session
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)


# Implement decorator here to reduce repetition
def login(s: Session) -> Tuple[str, str]:
    try:
        with open("config.json", "r") as file:
            login_data: Dict[str, str] = json.load(file)
            base_url = login_data.pop("base_url")

    except FileNotFoundError:
        print("Not yet setup yet")
        exit(1)

    args = sys.argv

    if len(args) == 1:
        print("No question selected")
        exit(1)

    index = f"{int(args[1]):03}"

    s.post(f"{base_url}/Login", login_data, verify=False)

    return base_url, index


def checkStatus(s: Session, base_url: str, index: str):
    r = s.get(f"{base_url}/HomeworkBoard")

    soup = BeautifulSoup(r.content.decode(), "html5lib")
    res: Tag = soup.find_all("tr")[int(index)]

    if res:
        elements = [i.get_text().strip() for i in res.find_all("td")]

        print(elements)

        testStatus = {
            "未繳": -1,
            "通過": 1,
            "未通過": 0,
        }

    isOpen = 0  # closed | now open | not yet open
    hasPassed = 0  # n/a | failed | passed
