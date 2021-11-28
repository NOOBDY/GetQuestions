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


class Colors:
    DEFAULT = "\033[0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"


def show_status(q_status: dict, t_status: dict) -> None:
    r_scolor =\
        Colors.GREEN if q_status['release_status'] == "Open" else\
        Colors.YELLOW if q_status['release_status'] == "Preparing" else\
        Colors.RED

    print(
        f"Realese Status: {r_scolor}{q_status['release_status']}{Colors.DEFAULT}, Due: {q_status['duo_date']}")
    print("Test Status:")

    passed = 0
    failed = 0

    for case in t_status:
        if t_status[case]:
            print(f" Case {case} {Colors.GREEN}v{Colors.DEFAULT}")
            passed += 1
        else:
            print(f" Case {case} {Colors.RED}x{Colors.DEFAULT}")
            failed += 1
    print(f"{Colors.GREEN}{passed} passed, {Colors.RED}{failed} failed, {Colors.DEFAULT}{len(t_status)} total")


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

            if f"{args[1]} {args[2]}" == "get all":
                question_statuses = s.get_question_statuses()
                print(
                    f"Index  Realease Status  {'Duo Date':<17}  Submit Status")
                for key in question_statuses:
                    a = question_statuses[key]
                    print(
                        f"{key:>5}  {a['release_status']:<15}  {a['duo_date']:<17}  {a['submit_status']}")
                exit(1)

            if args[1] == "get":
                index = args[2].rjust(3, '0')
                content = s.get(index)
                q_status = s.get_question_statuses()[index]
                t_status = s.get_test_status(login_data['name'], index)
                print(content)
                print("-" * 50)
                show_status(q_status, t_status)
                exit(1)

            if args[1] == "submit":
                index = args[2].rjust(3, '0')
                file_path = args[3]
                s.delete(index)
                s.submit(index, file_path)
                print("Submit success.")
                q_status = s.get_question_statuses()[index]
                t_status = s.get_test_status(login_data['name'], index)
                print("-" * 50)
                show_status(q_status, t_status)
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
