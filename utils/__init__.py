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

from ._login import _login
from ._status import _statuses
from ._get import _get
from ._submit import _submit, _delete


class JykuoSession:
    def __init__(self, base_url: str):
        self.session = Session()
        self.base_url = base_url

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        return Session.__exit__(
            self.session,
            exception_type,
            exception_value,
            traceback)

    login = _login
    get = _get
    get_question_statuses = _statuses
    submit = _submit
    delete = _delete


if __name__ == "__main__":
    print("Don't execute this file directly")
    exit(0)
