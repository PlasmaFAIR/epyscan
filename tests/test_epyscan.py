import epyscan


def test_make_run_dirs(tmp_path):
    path = epyscan.rundir_hierarchy(tmp_path, 1234)

    expected_path = tmp_path / "run_0_1000000/run_0_10000/run_1200_1300/run_1234"

    assert expected_path.is_dir()
    assert expected_path.exists()
