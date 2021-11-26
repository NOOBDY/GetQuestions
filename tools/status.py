import json
import time
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag
from dateutil import parser
from requests import Session


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
            release_status = f"Not Yet Open"

        elif info[4] == "準備中":
            release_status = f"Preparing"

        elif time() - release_time > 0:
            release_status = f"Closed"

        else:
            release_status = f"Now Open"

        print()
        print(f"Release Status: {release_status}")
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
            print(f" Case {case} x")
            failed += 1
        else:
            print(f" Case {case} v")
            passed += 1

    print()
    print(f"FAIL" if failed != 0 else f"PASS")
    print(f"{passed} passed, {failed} failed, {len(res)} total")
