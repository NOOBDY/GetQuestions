from bs4 import BeautifulSoup


def _get(self, index: str) -> str:
    session = self.session
    base_url = self.base_url

    r = session.get(f"{base_url}/showHomework?hwId={index}")
    if not r.ok:
        raise Exception("QuestionNotFoundError")

    soup = BeautifulSoup(r.content.decode(), "html5lib")
    res = soup.find(
        "span",
        style="font-family:標楷體; color:black; behavior:slide; word-wrap:break-word; word-break:normal; font-weight:bold; font-size:medium;")

    if res:
        context = ""
        for line in res.text.strip().split('\n'):
            context += line.strip() + "\n"
        return context
    else:
        raise Exception("Webpage probably changed")
