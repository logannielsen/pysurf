import json

from pysurf.helpers import http_get, requests


def test_requests_session_has_ua_header_set():
    assert not requests.headers["User-Agent"].startswith("python-requests")


def test_http_get():
    assert (
        json.loads(http_get("https://httpbin.org/get"))["url"]
        == "https://httpbin.org/get"
    )
