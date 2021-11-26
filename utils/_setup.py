import json
from getpass import getpass


def setup():
    _id = input("學號: ")
    passwd = getpass("密碼: ")

    with open("config.json", "w+") as file:
        config = {}

        config["name"] = _id
        config["passwd"] = passwd
        config["rdoCourse"] = "5"
        config["base_url"] = f"https://140.124.181.{'36' if int(_id[-3:]) % 2 == 1 else '39'}/upload"

        file.writelines(json.dumps(config, indent=4))
