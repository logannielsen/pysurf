import os
from unittest.mock import MagicMock

import pytest
from pysurf.data_process import Calendar

HERE = os.path.abspath(os.path.dirname(__file__))


def test_finds_all_calendar_events():
    get_tourn_html_fn = MagicMock(return_value="<a></a>")
    # total 57
    # unfinished 10
    with open(
        os.path.join(HERE, "resources", "mqs_cal_2019.html"), encoding="utf8"
    ) as f:
        cal = Calendar(f.read())
    # pulls all tourns through generator
    list(cal.completed_tourns(get_tourn_html_fn))
    assert get_tourn_html_fn.call_count == 47


@pytest.mark.parametrize(
    "fn, res", [("mct_cal_2014.html", True), ("mqs_cal_2019.html", False)]
)
def test_calendar_complete_property(fn, res):
    with open(os.path.join(HERE, "resources", fn), "r", encoding="utf8") as f:
        cal = Calendar(f.read())
    assert cal.completed is res
