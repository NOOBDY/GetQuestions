from typing import Dict, List, Tuple


def _login(self, login_data: Dict[str, str]) -> Tuple[str, str]:
    session = self.session
    base_url = self.base_url

    session.post(f"{base_url}/Login", login_data, verify=False, timeout=2)
    session.get(f"{base_url}/MainMenu")


if __name__ == "__main__":
    print("Don't execute this file directly")
    exit(0)
