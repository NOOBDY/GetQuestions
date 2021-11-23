import json
from time import time

from requests import Session


# i will repurpose this for checking if the test passed

def submit(s: Session, base_url: str, index: str, filepath: str):
    try:
        file = open(filepath, "r")

    except FileNotFoundError:
        print("Can't find specified file")
        exit(1)

    filename = f"{json.load(open('config.json'))['name']}_{index}_{round(time() * 1000)}.py"

    url = f"{base_url}/upLoadHw?hwId={index}&l=Python"

    # delete original file first to overwrite
    # calling delete on unsubmitted files are fine
    s.get(f"{url}/delHw?title={index}")

    # after digging around i discovered i need to have a GET request first? WTF???
    # maybe it stores a cookie or some shit
    s.get(url).content.decode()

    post_response = s.post(f"{base_url}/upLoadFile",
                           files={"hwFile": (filename, file, "text/x-python")}).json()

    if post_response["success"]:
        print("Upload success")
        # do passing check here
    else:
        print(post_response["errorMSg"])
