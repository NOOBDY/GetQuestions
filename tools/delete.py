from requests import Session


def delete(s: Session, url: str, index: str):
    s.get(f"{url}/delHw?title={index}")
