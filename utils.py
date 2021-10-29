import json
import sys
from typing import Dict, Tuple

from requests import Session
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)


# Implement decorator here to reduce repetition
def login(s: Session) -> Tuple[str, str]:
    try:
        with open("login.json", "r") as json_file:
            login_data: Dict[str, str] = json.load(json_file)

        with open("config.txt", "r") as config:
            base_url = f"https://140.124.181.{config.readline()}/upload"

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
