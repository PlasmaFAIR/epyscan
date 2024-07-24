import epyscan
import epydeck

import numpy as np


def test_make_run_dirs(tmp_path):
    path = epyscan.rundir_hierarchy(tmp_path, 1234)

    expected_path = tmp_path / "run_0_1000000/run_0_10000/run_1200_1300/run_1234"

    assert expected_path.is_dir()
    assert expected_path.exists()


def test_expand_flatdict():
    flatdict = {
        "a:b:c": 1,
        "a:b:d": 2,
        "a:e:f": 3,
        "a:e:g": 4,
        "h:i": 5,
        "h:j": 6,
    }

    expected = {
        "a": {
            "b": {"c": 1, "d": 2},
            "e": {"f": 3, "g": 4},
        },
        "h": {"i": 5, "j": 6},
    }

    result = epyscan.expand_flatdict(flatdict)
    assert result == expected


def test_gridscan():
    parameters = {
        "block:var1": {"min": 1.0e1, "max": 1.0e4, "log": True},
        "block:var2": {"min": 2.0, "max": 5.0},
    }

    grid_scan = epyscan.GridScan(parameters, n_samples=4)
    samples = list(grid_scan)

    expected = [
        {"block:var1": 1.0e1, "block:var2": 2.0},
        {"block:var1": 1.0e1, "block:var2": 3.0},
        {"block:var1": 1.0e1, "block:var2": 4.0},
        {"block:var1": 1.0e1, "block:var2": 5.0},
        {"block:var1": 1.0e2, "block:var2": 2.0},
        {"block:var1": 1.0e2, "block:var2": 3.0},
        {"block:var1": 1.0e2, "block:var2": 4.0},
        {"block:var1": 1.0e2, "block:var2": 5.0},
        {"block:var1": 1.0e3, "block:var2": 2.0},
        {"block:var1": 1.0e3, "block:var2": 3.0},
        {"block:var1": 1.0e3, "block:var2": 4.0},
        {"block:var1": 1.0e3, "block:var2": 5.0},
        {"block:var1": 1.0e4, "block:var2": 2.0},
        {"block:var1": 1.0e4, "block:var2": 3.0},
        {"block:var1": 1.0e4, "block:var2": 4.0},
        {"block:var1": 1.0e4, "block:var2": 5.0},
    ]

    assert samples == expected


def test_campaign(tmp_path):
    parameters = {
        "block:var1": {"min": 1.0e1, "max": 1.0e4, "log": True},
        "block:var2": {"min": 2.0, "max": 5.0},
    }

    grid_scan = epyscan.GridScan(parameters, n_samples=4)
    template = {"block": {"var3": 1.23}, "other_block": {"var4": True}}
    campaign = epyscan.Campaign(template, tmp_path)

    paths = [campaign.setup_case(sample) for sample in grid_scan]

    base_path = tmp_path / "run_0_1000000/run_0_10000/run_0_100"

    expected_paths = [
        base_path / "run_0",
        base_path / "run_1",
        base_path / "run_2",
        base_path / "run_3",
        base_path / "run_4",
        base_path / "run_5",
        base_path / "run_6",
        base_path / "run_7",
        base_path / "run_8",
        base_path / "run_9",
        base_path / "run_10",
        base_path / "run_11",
        base_path / "run_12",
        base_path / "run_13",
        base_path / "run_14",
        base_path / "run_15",
    ]

    assert paths == expected_paths

    expected_case_deck = {
        "block": {"var1": 1e2, "var2": 2.0, "var3": 1.23},
        "other_block": {"var4": True},
    }

    with open(base_path / "run_4" / "input.deck") as f:
        actual_case_deck = epydeck.load(f)

    assert actual_case_deck == expected_case_deck
