from typing import Dict, Tuple
import json


def init(index: str) -> Dict[str, str]:
    try:
        with open("config.json", "r") as file:
            login_data: Dict[str, str] = json.load(file)
            login_data["index"] = f"{int(index):03}"
            print(login_data)

        return login_data

    except FileNotFoundError:
        raise FileNotFoundError
