import os

from pysurf.data_process import HeatData

HERE = os.path.abspath(os.path.dirname(__file__))


def test_yielding_tourn_ids():
    with open(
        os.path.join(HERE, "resources", "mcs_json_heat_res.json"),
        encoding="utf8",
    ) as f:

        heat = HeatData.from_json(f.read())
        assert heat.event_name == "Quiksilver Pro Gold Coast"
        assert heat.name == "Round 1, Heat 1"
        assert heat.heat_status == "Completed"
        assert heat.date == "April 2, 2019"
        assert heat.beach == "Duranbah"
        assert heat.duration == 30
        assert heat.wave_min == 4
        assert heat.wave_max == 6
        assert heat.wind_conditions == "Light"
        assert heat.total_waves == 27
        assert heat.avg_heat_score == 9.44
