from typing import Dict

import urllib3
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)


def _get_test_status(self, id_: int, index: str) -> Dict[str, bool]:
    session = self.session
    base_url = self.base_url

    # you can check other people's upload status while logged in lol
    res = session.get(
        f"{base_url}/CheckResult?questionID={index}&studentID={id_}")

    soup = BeautifulSoup(res.content.decode(), "html5lib")

    cases = {}
    for test in list(soup.find_all("tr"))[1:]:
        case, status = [i.get_text().strip() for i in test.find_all("td")]
        cases[case] = status != '測試失敗'

    return cases
