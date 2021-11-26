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

from utils import JykuoSession
from utils._setup import setup

urllib3.disable_warnings()

if __name__ == '__main__':
    args = sys.argv

    if args[1] == "setup":
        setup()
        exit(1)

    try:
        with open("./config.json", "r") as file:
            login_data = json.load(file)
            base_url = login_data.pop("base_url")

    except FileNotFoundError:
        print("Not yet setup yet")
        exit(1)

    with JykuoSession(base_url) as s:
        try:
            s.login(login_data)
            if args[1] == "get":
                index = args[2].rjust(3, '0')
                content = s.get(index)
                print(content)

                exit(1)
            if args[1] == "submit":
                index = args[2].rjust(3, '0')
                file_path = args[3]
                s.delete(index)
                s.submit(index, file_path)
                print("Submit success.")
                exit(1)

        except ConnectTimeout:
            print("Not connected to school network")
            exit(1)

        except SSLError:
            print("Wrong username or password")
            exit(1)
        except FileNotFoundError:
            print("SubmittedFileNotFound")
            exit(1)
