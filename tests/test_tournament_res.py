import os
from unittest.mock import MagicMock

import pytest
from pysurf.data_process import Tournament

HERE = os.path.abspath(os.path.dirname(__file__))


@pytest.mark.parametrize(
    "fn, tourn_name, tourn_start",
    [("wct_tourn_res_2019.html", "Boost Mobile Pro Gold Coast", "Apr 3")],
)
def test_tournament_name(fn, tourn_name, tourn_start):
    with open(os.path.join(HERE, "resources", fn), "r", encoding="utf8") as f:
        tourn = Tournament(f.read())
    assert tourn.name == tourn_name
    assert tourn.start_date == tourn_start


def test_rounds_function():
    get_round_html = MagicMock(return_value="<a></a>")
    with open(
        os.path.join(HERE, "resources", "wct_tourn_res_2019.html"),
        encoding="utf8",
    ) as f:
        tourn = Tournament(f.read())
    # pulls all tourns through generator
    list(tourn.rounds(get_round_html))
    assert get_round_html.call_count == 6
