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

def _statuses(self) -> Dict[str, Dict[str, str]]:
    session = self.session
    base_url = self.base_url

    res = session.get(f"{base_url}/HomeworkBoard")
    soup = BeautifulSoup(res.content.decode(), "html5lib")

    question_statuses = {}
    for tr in soup.find_all("tr"):
        # [index, hw_type, padded_index, due_date, submit_button, language, pass_status, check_result, passed_list]
        info = [i.get_text().strip() for i in tr.find_all("td")]
    
        if len(info) == 0:
            continue

        release_time = parser.parse(info[3]).timestamp()

        # CLOSED | OPEN | NOT_OPEN_YET | PREPARING
        # that number is the default time
        release_status =\
        "NOT_OPEN_YET" if info[3] == "2021/09/20 23:59" else\
        "PREPARING" if info[4] == "準備中" else\
        "CLOSED" if time() - release_time > 0 else\
        "OPEN"

        # PASS | FAILED | DID_NOT_SUBMIT
        submit_status =\
        "PASS" if info[6] == "通過" else\
        "FAIL" if info[6] == "未通過" else\
        "DID_NOT_SUBMIT"

        question_statuses[info[0]] = {
            "release_status": release_status,
            "duo_date": info[3] if release_status != "NOT_YET_OPEN" else "Not Open Yet",
            "submit_status": submit_status,
        }
    return question_statuses

if __name__ == "__main__":
    print("Don't execute this file directly")
    exit(0)
