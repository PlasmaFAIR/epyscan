# epyscan

Create campaigns of EPOCH runs over a given parameter space using
different sampling methods

This is a work in progress, with only uniform grid scans implemented
so far.

## Examples

Parameter space to be sampled is described by a `dict` where keys
should be in the form of `block_name:parameter`, and values should
be dicts with the following keys:

- `"min"`: minimum value of the parameter
- `"max"`: maximum value of the parameter
- `"log"`: (optional) `bool`, if `True` then grid is done in
  log space for this parameter

```python
```python
import pathlib
import epyscan
import epydeck

# Define the parameter space to be sampled. Here, we are varying the intensity and density.
parameters = {
  "constant:intens": {"min": 1.0e22, "max": 1.0e24, "log": True},  # Intensity varies logarithmically between 1.0e22 and 1.0e24
  "constant:nel": {"min": 1.0e20, "max": 1e24, "log": True},       # Density varies logarithmically between 1.0e20 and 1.0e24
}

# Load a deck file to use as a template for the simulations
with open("template_deck_filename") as f:
  deck = epydeck.load(f)

# Create a grid scan object that will generate 4 different sets of parameters within the specified ranges
grid_scan = epyscan.GridScan(parameters, n_samples=4)

# Define the root directory where the simulation folders will be saved. This directory will be created if it doesn't exist.
run_root = pathlib.Path("example_campaign")

# Initialize a campaign object with the template deck and the root directory. This will manage the creation of simulation cases.
campaign = epyscan.Campaign(deck, run_root)

# Generate the folders and deck files for each set of parameters in the grid scan
paths = [campaign.setup_case(sample) for sample in grid_scan]

# Save the paths of the generated simulation folders to a file
with open("paths.txt", "w") as f:
  [f.write(str(path) + "\n") for path in paths]

# Opening paths.txt
# /users/bmp535/scratch/paper/1d_intens_vs_nel_v3_test/run_0_1000000/run_0_10000/run_0_100/run_0
# /users/bmp535/scratch/paper/1d_intens_vs_nel_v3_test/run_0_1000000/run_0_10000/run_0_100/run_1
# /users/bmp535/scratch/paper/1d_intens_vs_nel_v3_test/run_0_1000000/run_0_10000/run_0_100/run_2
# /users/bmp535/scratch/paper/1d_intens_vs_nel_v3_test/run_0_1000000/run_0_10000/run_0_100/run_3
```
