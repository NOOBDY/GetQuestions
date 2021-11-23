from typing import Dict

import urllib3
from requests import Session
from requests.exceptions import ConnectTimeout, SSLError
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)


# Implement decorator here to reduce repetition
def login(s: Session, login_data: Dict[str, str]) -> None:
    base_url = login_data["base_url"]

    try:
        s.post(f"{base_url}/Login", login_data, verify=False, timeout=2)
        s.get(f"{base_url}/MainMenu")

    except ConnectTimeout:
        print("Not connected to school network")
        raise ConnectTimeout

    except SSLError:
        print("Wrong username or password")
        raise SSLError
