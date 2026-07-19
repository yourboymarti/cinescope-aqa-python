import json
import logging
import os
import time
import requests
from pydantic import BaseModel


class CustomRequester:
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()
        # self.headers = self.base_headers
        self.session.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)

    def send_request(self, method, endpoint, data=None, params=None, expected_status=200, need_logging=True, **kwargs):
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()

        if isinstance(data, BaseModel):
            data = json.loads(data.model_dump_json(exclude_unset=True))
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            **kwargs
        )

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        if need_logging:
            self.log_request_and_response(response, elapsed_ms)

        if response.status_code != expected_status:
            raise ValueError(
                f"Unexpected status code: {response.status_code}. "
                f"Expected: {expected_status}. "
                f"Response: {response.text}"
            )

        return response

    def _update_session_headers(self, headers: dict):
        self.session.headers.update(headers)

    def log_request_and_response(self, response, elapsed_ms):
        try:
            request = response.request

            green = "\033[32m"
            red = "\033[31m"
            reset = "\033[0m"

            full_test_name = (
                f"pytest "
                f"{os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"
            )

            headers = " \\\n".join(
                [
                    f"-H '{header}: {value}'"
                    for header, value in request.headers.items()
                ]
            )

            body = ""

            if request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode("utf-8")
                elif isinstance(request.body, str):
                    body = request.body

                if body and body != "{}":
                    body = f"-d '{body}'"

            self.logger.info(
                f"\n{'=' * 40} REQUEST {'=' * 40}"
            )

            self.logger.info(
                f"{green}{full_test_name}{reset}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_status = response.status_code
            response_data = response.text

            try:
                response_data = json.dumps(
                    json.loads(response.text),
                    indent=4,
                    ensure_ascii=False
                )
            except json.JSONDecodeError:
                pass

            self.logger.info(
                f"\n{'=' * 40} RESPONSE {'=' * 40}"
            )

            if response.ok:
                self.logger.info(
                    f"\tSTATUS_CODE: "
                    f"{green}{response_status}{reset}\n"
                    f"\tTIME: {elapsed_ms} ms\n"
                    f"\tDATA:\n{response_data}"
                )
            else:
                self.logger.info(
                    f"\tSTATUS_CODE: "
                    f"{red}{response_status}{reset}\n"
                    f"\tTIME: {elapsed_ms} ms\n"
                    f"\tDATA: {red}{response_data}{reset}"
                )

            self.logger.info(f"{'=' * 80}\n")

        except Exception as error:
            self.logger.error(
                f"\nLogging failed: {type(error)} - {error}"
            )

    def _reset_headers(self):
        self.session.headers.clear()
        self.session.headers.update(self.headers)



auth_session = requests.Session()
requester_auth = CustomRequester(
    session=auth_session,
    base_url="https://auth.dev-cinescope.coconutqa.ru"
)
