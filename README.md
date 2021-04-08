# sckernel

sckernel is a Jupyter Notebook kernel for SuperCollider's sclang.  sckernel
launches a post window to display output just as the SuperCollider IDE does
while the Notebook front end handles input.

Syntax highlighting in the Notebook uses smalltalk as a default.

At this stage sckernel has only been tested on MacOS and is only guaranteed
to work on that operating system.  sckernel **may** work on other platforms
but has not been tested yet.

## Requirements

In order for sckernel to work, the binary `sclang` must be in your $PATH.

## Installation

To install `sckernel` from PyPI:

```
pip install sckernel
python -m sckernel.install
```

By default the kernel will be install in the per-user kernel registry,
equivalent to `python -m sckernel.install --user`.

To install in the root directory or for an environment like Anaconda or
venv, run instead `python -m sckernel.install --sys-prefix`.

## Using SuperCollider kernel

When opening Jupyter notebook, select from the <i>New</i> menu SC_Kernel to create
a new SuperCollider notebook using sclang.

For the console frontend, you can run it by adding `--kernel sckernel`.

## Converting from Notebooks to SuperCollider files (.scd)

The sckernel package also comes with a convenience script to translate
from Jupyter notebooks to .scd files (i.e., SuperCollider files).  

```
python -m sckernel.convertNotebookToScd /path/to/notebook /path/to/destination
```

Some light formatting is done to make the .scd files readable in a similar way
to Jupyter Notebooks.
