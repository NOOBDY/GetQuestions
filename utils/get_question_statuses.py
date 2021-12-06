from time import time
from typing import Dict

import urllib3
from bs4 import BeautifulSoup
from dateutil import parser
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)


def _get_question_statuses(self) -> Dict[str, Dict[str, str]]:
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

        # that number is the default time
        release_status =\
            "Not Open Yet" if info[3] == "2021/09/20 23:59" else\
            "Preparing" if info[4] == "準備中" else\
            "Closed" if time() - release_time > 0 else\
            "Open"

        submit_status =\
            "Pass" if info[6] == "通過" else\
            "Fail" if info[6] == "未通過" else\
            "Did Not Submit"

        question_statuses[info[2]] = {
            "release_status": release_status,
            "duo_date": info[3] if release_status != "Not Open Yet" else "Not Open Yet",
            "submit_status": submit_status,
        }
    return question_statuses
