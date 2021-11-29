#!/usr/bin/env python
import json
from time import time

import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)

def _delete(self, index: str) -> None:
    session = self.session
    base_url = self.base_url
    session.get(f"{base_url}/delHw?title={index}")


def _submit(self, index: str, filepath: str) -> None:
    session = self.session
    base_url = self.base_url

    try:
        file = open(filepath, "r")
    except FileNotFoundError:
        print("Can't find specified file")
        exit(1)

    filename = f"{json.load(open('config.json'))['name']}_{index}_{round(time() * 1000)}.py"

    url = f"{base_url}/upLoadHw?hwId={index}&l=Python"
    # after digging around i discovered i need to have a GET request first? WTF???
    # maybe it stores a cookie or some shit
    get_response = session.get(url).content.decode()

    post_response = session.post(
        f"{base_url}/upLoadFile",
        files={
            "hwFile": (
                filename,
                file,
                "text/x-python")}).json()

    if not post_response["success"]:
        raise Exception(post_response["errorMSg"])


if __name__ == "__main__":
    print("Don't execute this file directly")
    exit(0)
