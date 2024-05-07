from pathlib import Path


def rundir_hierarchy(root: Path, run_num: int) -> Path:
    """Create nested directory structure for a run"""

    def level_dir(exponent: int) -> Path:
        level = 100**exponent
        return Path(
            f"run_{int(run_num / level) * level}_{int(run_num / level + 1) * level}"
        )

    level_1_dir = level_dir(3)
    level_2_dir = level_dir(2)
    level_3_dir = level_dir(1)
    level_4_dir = f"run_{run_num}"

    path = root / level_1_dir / level_2_dir / level_3_dir / level_4_dir
    path.mkdir(parents=True, exist_ok=True)
    return path
