epyscan
=======

Create campaigns of EPOCH runs over a given parameter space using
different sampling methods

This is a work in progress, with only uniform grid scans implemented
so far.

Examples
--------

Parameter space to be sampled is described by a `dict` where keys
should be in the form of `block_name:parameter`, and values should
be dicts with the following keys:

- `"min"`: minimum value of the parameter
- `"max"`: maximum value of the parameter
- `"log"`: (optional) `bool`, if `True` then grid is done in
  log space for this parameter


```python
import epyscan
import pathlib

# Description of parameter space
parameters = {
    "block:var1": {"min": 1.0e1, "max": 1.0e4, "log": True},
    "block:var2": {"min": 2.0, "max": 5.0},
}

# Template of deck file
template = {"block": {"var3": 1.23}, "other_block": {"var4": True}}

# Sets up iterator for specific parameters and specifies number of samples to split data across
grid_scan = epyscan.GridScan(parameters, n_samples=4)

# Location of folder to save simulations to
run_root = pathlib.Path("example_campaign")

# Takes in the folder and template and starts a counter so each new simulation gets saved to a new folder
campaign = epyscan.Campaign(template, run_root)

# Create the folders and deck files
paths = [campaign.setup_case(sample) for sample in grid_scan]

# Prints the output of the last created deck file
with open(paths[-1] / "input.deck") as f:
    print(f.read())

# begin:block
#   var3 = 1.23
#   var1 = 100.0
#   var2 = 2.0
# end:block
#
# begin:other_block
#   var4 = T
# end:other_block

```
