import epydeck

from pathlib import Path
import numpy as np

from typing import Union


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


def _expand_flatkey(flat_key: str, value) -> dict:
    key_parts = flat_key.split(":", maxsplit=1)
    if len(key_parts) > 1:
        value = _expand_flatkey(key_parts[1], value)
    return {key_parts[0]: value}


def expand_flatdict(flat_dict: dict) -> dict:
    result = {}
    for key, value in flat_dict.items():
        result = epydeck.deep_update(result, _expand_flatkey(key, value))

    return result


class Campaign:
    """Campaign of runs based on a template dict

    Used to create specific cases from samples of parameter space

    Arguments
    ---------
    template:
        Base template deck as a Python dict (for example, as created by `epydeck`)
    root:
        Path to root run directory

    Examples
    --------

    >>> with open("template.deck") as f:
            template = epydeck.load(f)
    >>> campaign = Campaign(template, "grid_root")
    >>> path = campaign.setup_case({"constant:lambda": 1.e-6})

    """

    def __init__(self, template: dict, root: Union[str, Path]):
        self._counter = 0
        self.template = template
        self.root = Path(root)

    def setup_case(self, sample: dict):
        """Create run directory with input deck for given sample

        Parameters
        ----------
        sample : dict
            Dict of specific parameter values to apply to base
            template

        """

        expanded_sample_dict = expand_flatdict(sample)
        full_sample = epydeck.deep_update(self.template, expanded_sample_dict)
        path = rundir_hierarchy(self.root, self._counter)

        with open(path / "input.in", "w") as f:
            epydeck.dump(full_sample, f)

        self._counter += 1
        return path


class GridScan:
    """Uniform sampling of the Cartesian outer product of the parameter ranges

    Arguments
    ---------
    parameters:
        Mapping of parameters to ranges. Keys should be in the form of
        `block_name:parameter`, while values should be dicts with the
        following keys:

        - `"min"`: minimum value of the parameter
        - `"max"`: maximum value of the parameter
        - `"log"`: (optional) `bool`, if `True` then grid is done in
          log space for this parameter

    n_samples:
        Number of samples in each dimension

    Examples
    --------
    >>> parameters = {
          "block:var1": {"min": 1.0e1, "max": 1.0e4, "log": True},
          "block:var2": {"min": 2.0, "max": 5.0},
        }
    >>> grid_scan = GridScan(parameters, n_samples=4)
    >>> next(grid_scan)
    {'block:var1': 10.0, 'block:var2': 2.0}

    """

    def __init__(self, parameters: dict, n_samples: int = 10):

        def _gridspace(start, stop, num: int, log=False):
            """Generalisation over logspace/linspace"""
            if log:
                return np.logspace(np.log10(start), np.log10(stop), num=num)

            return np.linspace(start, stop, num=num)

        self.parameters = {
            k: _gridspace(v["min"], v["max"], num=n_samples, log=v.get("log", False))
            for k, v in parameters.items()
        }

        grids = np.meshgrid(*self.parameters.values(), indexing="ij")

        self._samples = [
            dict(zip(parameters.keys(), sample))
            for sample in zip(*(grid.flat for grid in grids))
        ]

        self._n_samples = len(self._samples)
        self._sample_iter = iter(self._samples)

    def __len__(self) -> int:
        return self._n_samples

    def __iter__(self):
        return self._sample_iter

    def __next__(self):
        return next(self._sample_iter)

    def sample(self, num: int = 1):
        if num == 1:
            return next(self)

        return [sample for (sample, _) in zip(self, range(num))]
