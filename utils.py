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
