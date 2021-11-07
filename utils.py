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
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)


class Colors:
    DEFAULT = "\033[0m"
    PASSED = "\033[92m"
    FAILED = "\033[91m"


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
        # [index, hw_type, padded_index, due_date, submit_button, pass_status, check_result, passed_list]
        elements = [i.get_text().strip() for i in res.find_all("td")]

        release_status = ""  # Closed | Now Open | Not Yet Open

        release_time = parser.parse(elements[3]).timestamp()

        # that number is the default time
        if release_time == 1633017540.0 or elements[4] == "準備中":
            release_status = "Not Yet Open"

        elif time() - release_time > 0:
            release_status = "Closed"

        else:
            release_status = "Now Open"

        print()
        print(f"Release Status: {release_status}", end="")
        print(f", Due: {elements[3]}" if release_status == "Now Open" else "")
        print()
        if release_status != "Not Yet Open":
            test_status(s, base_url, index)


def test_status(s: Session, base_url: str, index: str) -> None:
    with open("config.json") as file:
        _id = json.load(file)["name"]

    # you can check other people's upload status while logged in lol
    r = s.get(
        f"{base_url}/CheckResult?questionID={index}&studentID={_id}")

    soup = BeautifulSoup(r.content.decode(), "html5lib")
    res: List[Tag] = list(soup.find_all("tr"))[1:]

    passed = 0
    failed = 0

    for test in res:
        case, status = [i.get_text().strip() for i in test.find_all("td")]
        if status == '測試失敗':
            print(Colors.FAILED + f"Case {case}: Failed")
            failed += 1
        else:
            print(Colors.PASSED + f"Case {case}: Passed")
            passed += 1

    print(Colors.DEFAULT + f"\n{passed} passed, {failed} failed")


if __name__ == "__main__":
    print("Don't execute this file directly")
    exit(0)
