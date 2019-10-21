import os

import pytest
from pysurf.data_process import TournRound

HERE = os.path.abspath(os.path.dirname(__file__))


@pytest.mark.parametrize(
    "fn, first_heat_id",
    [
        ("wct_tourn_round_res_2019.html", 75707),
        ("mqs_tourn_round_res_2017.html", 45783),
    ],
)
def test_yielding_tourn_ids(fn, first_heat_id):
    with open(os.path.join(HERE, "resources", fn), encoding="utf8") as f:
        round_res = TournRound(f.read())
        print(type(next(round_res.heat_id_generator())))
    assert next(round_res.heat_id_generator()) == first_heat_id
