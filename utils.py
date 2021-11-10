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
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"


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
        # [index, hw_type, padded_index, due_date, submit_button, language, pass_status, check_result, passed_list]
        info = [i.get_text().strip() for i in res.find_all("td")]

        release_status = ""  # Closed | Now Open | Not Yet Open | Preparing

        release_time = parser.parse(info[3]).timestamp()

        # that number is the default time
        if release_time == 1633017540.0:
            release_status = f"{Colors.RED}Not Yet Open"

        elif info[4] == "準備中":
            release_status = f"{Colors.YELLOW}Preparing"

        elif time() - release_time > 0:
            release_status = f"{Colors.RED}Closed"

        else:
            release_status = f"{Colors.GREEN}Now Open"

        print()
        print(f"Release Status: {release_status}", end=f"{Colors.DEFAULT}")
        release_status = release_status[5:]  # remove color characters
        print(f", Due: {info[3]}" if release_status != "Not Yet Open" else "")
        print("Test Status: ", end="")

        if info[6] == "未繳":
            print("Haven't Submitted")
            return

        if release_status != "Not Yet Open":
            print("\n")
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
            print(f" {Colors.DEFAULT}Case {case} {Colors.RED}x")
            failed += 1
        else:
            print(f" {Colors.DEFAULT}Case {case} {Colors.GREEN}v")
            passed += 1

    print()
    print(f"{Colors.RED}FAIL" if failed != 0 else f"{Colors.GREEN}PASS")
    print(f"{Colors.DEFAULT}{passed} passed, {failed} failed, {len(res)} total")


if __name__ == "__main__":
    print("Don't execute this file directly")
    exit(0)
