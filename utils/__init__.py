from requests import Session

from .login import _login
from .get_question_statuses import _get_question_statuses
from .get_test_status import _get_test_status
from .get import _get
from .submit import _submit, _delete


class JykuoSession:
    def __init__(self, base_url: str):
        self.session = Session()
        self.base_url = base_url

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        return Session.__exit__(
            self.session,
            exception_type,
            exception_value,
            traceback)

    login = _login
    get = _get
    get_question_statuses = _get_question_statuses
    get_test_status = _get_test_status
    submit = _submit
    delete = _delete
