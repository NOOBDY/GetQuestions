import json
import sys
from time import time
from typing import Dict, Tuple

import urllib3
from bs4 import BeautifulSoup
from bs4.element import Tag
from dateutil import parser
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


def status(s: Session, base_url: str, index: str) -> None:
    r = s.get(f"{base_url}/HomeworkBoard")

    soup = BeautifulSoup(r.content.decode(), "html5lib")
    res: Tag = soup.find_all("tr")[int(index)]

    if res:
        elements = [i.get_text().strip() for i in res.find_all("td")]

        print(elements)

        release_status = ""  # Closed | Now Open | Not Yet Open

        test_status = {
            "未繳": "N/A",
            "通過": "Passed",
            "未通過": "failed",
        }

        release_time = parser.parse(elements[3]).timestamp()

        if release_time == 1633017540.0 or elements[4] == "準備中":
            release_status = "Not Yet Open"

        elif time() - release_time > 0:
            release_status = "Closed"

        else:
            release_status = "Now Open"

        print(f"Release Status: {release_status}")
        print(f"Test Status: {test_status[elements[6]]}")


if __name__ == "__main__":
    print("Don't execute this file directly")
    exit(0)
