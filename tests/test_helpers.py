import json
import os
import types
from pathlib import Path
from unittest.mock import mock_open, patch

import bs4
import pysurf.helpers
import pytest
from requests.exceptions import RequestException


def test_requests_session_has_ua_header_set():
    requests = pysurf.helpers.requests
    assert not requests.headers["User-Agent"].startswith("python-requests")


def test_page_status():
    http_get_response = pysurf.helpers.http_get_response
    with pytest.raises(RequestException):
        http_get_response("https://httpbin.org/status/400")


def test_http_get_text():
    http_get_text = pysurf.helpers.http_get_text
    assert (
        json.loads(http_get_text("https://httpbin.org/get"))["url"]
        == "https://httpbin.org/get"
    )


@pytest.mark.parametrize(
    "test, result",
    [
        (
            "https://so.com/qs/247770/how-to-retrieve-a-modules-path",
            (Path("qs/247770/"), "how-to-retrieve-a-modules-path"),
        )
    ],
)
def test_file_path_creator(test, result):
    create_file_path = pysurf.helpers.create_file_path
    assert result == create_file_path(url=test)


@patch("pysurf.helpers.os.makedirs")
@patch("pysurf.helpers.os.path.exists", return_value=False)
def test_make_dirs_calls_os_makedirs_if_path_doesnt_exist(
    exists_mock, make_mock
):
    assert exists_mock is pysurf.helpers.os.path.exists
    assert make_mock is pysurf.helpers.os.makedirs
    pysurf.helpers.create_dirs("path")
    make_mock.assert_called_once_with("path")


@patch("pysurf.helpers.os.makedirs")
@patch("pysurf.helpers.os.path.exists", return_value=True)
def test_make_dirs_calls_os_makedirs_if_path_exists(exists_mock, make_mock):
    assert exists_mock is pysurf.helpers.os.path.exists
    assert make_mock is pysurf.helpers.os.makedirs
    pysurf.helpers.create_dirs("path")
    make_mock.assert_not_called()


def test_save_file_to_dir():
    m = mock_open()
    with patch("pysurf.helpers.open", m):
        pysurf.helpers.save_file(Path("a/b"), "filename", "req_text")
    m.mock_calls
    m.assert_called_once_with(Path("a/b/filename"), "w", encoding="utf-8")
    handle = m()
    handle.write.assert_called_once_with("req_text")


@pytest.fixture
def test_data():
    fn = os.path.join(os.path.dirname(__file__))
    f = pysurf.helpers.open_souped_file(fn, "mct_test_example")
    yield f


def test_yielding_completed_events(test_data):
    result = pysurf.helpers.yield_completed_events(test_data)
    assert isinstance(result, types.GeneratorType)
    for res in result:
        assert isinstance(res, bs4.element.Tag)
        assert res["class"] == any(
            [
                "tour-event tour-event--completed",
                "tour-event tour-event--completed tour-event--has-category",
                "tour-event tour-event--upcoming",
            ]
        )


def test_return_event_detail(test_data):
    result = pysurf.helpers.yield_completed_events(test_data)
    for res in result:
        tour_details = pysurf.helpers.produce_event_detail(res)
        assert isinstance(tour_details, bs4.element.Tag)
        assert tour_details["class"] == ["tour-event-detail"]


def test_getting_href(test_data):
    result = list(pysurf.helpers.get_href(test_data))
    assert result[
        0
    ] == "https://www.worldsurfleague.com/events/2019/mct/2908/"(
        "quiksilver-pro-gold-coast"
    )
    assert len(result) == 11
