from typing import Dict


def _login(self, login_data: Dict[str, str]) -> None:
    session = self.session
    base_url = self.base_url

    session.post(f"{base_url}/Login", login_data, verify=False, timeout=2)
    session.get(f"{base_url}/MainMenu")
