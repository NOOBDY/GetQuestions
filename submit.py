#!/usr/bin/env python
import json
import sys
from time import time

import urllib3
from requests import Session
from urllib3.exceptions import InsecureRequestWarning

from utils import checkStatus, login

urllib3.disable_warnings(category=InsecureRequestWarning)


# i will repurpose this for checking if the test passed
def delete(s: Session, url: str, index: str):
    s.get(f"{url}/delHw?title={index}")


def submit(s: Session, base_url: str, index: str, filepath: str):
    try:
        file = open(filepath, "r")

    except FileNotFoundError:
        print("Can't find specified file")
        exit(1)

    filename = f"{json.load(open('login.json'))['name']}_{index}_{round(time() * 1000)}.py"

    url = f"{base_url}/upLoadHw?hwId={index}&l=Python"
    # after digging around i discovered i need to have a GET request first? WTF???
    # maybe it stores a cookie or some shit
    get_response = s.get(url).content.decode()

    post_response = s.post(f"{base_url}/upLoadFile",
                           files={"hwFile": (filename, file, "text/x-python")}).json()

    if post_response["success"]:
        print("Upload success")
        # do passing check here
    else:
        print(post_response["errorMSg"])


if __name__ == "__main__":
    with Session() as s:
        base_url, index = login(s)
        # i discovered it doesn't matter if you call delete on a un-submitted question
        # i figured calling delete every time would probably be faster since the backend is so slow lmao
        # delete(s, base_url, index)
        # submit(s, base_url, index, sys.argv[2])

        checkStatus(s, base_url, index)
