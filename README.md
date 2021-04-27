# sckernel

sckernel is a Jupyter Notebook kernel for SuperCollider's sclang.  sckernel
launches a post window to display output just as the SuperCollider IDE does
while the Notebook front end handles input.

Syntax highlighting in the Notebook uses codemirror with a mode defined in
kernel.js.

sckernel has been tested on both MacOS and Windows 10.

## Requirements

Users need a working installation of SuperCollider and Jupyter Notebook.
There are several ways to install Jupyter Notebook as detailed at
www.jupyter.org/install.  The quickest way is by downloading Anaconda.

sckernel requires Python 3.5 or higher.  Please be sure if you downloaded
the Notebook through Anaconda that it is for Python 3.5 or higher.

## Installation

### Step 1: Download sckernel

To download `sckernel` from PyPI:

```
pip install sckernel
```

### Step 2: Install the kernelspec for sckernel

To complete the installation, you must select a location for the sckernel
configuration files (called a kernelspec).  There are three options:

1)  To install locally to your user account, run

    ```
    python -m sckernel.install
    ```

    The above line is also equivalent to `python -m sckernel.install --user`.

2) To install in the root directory or for an environment like Anaconda or
venv, run 

    `python -m sckernel.install --sys-prefix`.

3) To install to another location (not recommended), run

    ```
    python -m sckernel.install --prefix <your_prefix_path>
    ```

    sckernel's kernelspec will be installed in {PREFIX}/share/jupyter/kernels/.

### Step 3: Configure sckernel to find your Python and sclang binaries

sckernel works by launching two separate subprocesses: a post window implemented
in Python and sclang, the frontend interpreter for SuperCollider.  To launch
these processes properly, sckernel needs to know where to find those binaries.
To complete the installation, run the following with those paths:

```
python -m sckernel.config --python /path/to/python --sclang /path/to/sclang
```

You may omit this step entirely.  By default, sckernel will attempt to search
through your PATH environment variable for the first instance of `python` and `sclang`
and attempt to run those.  Depending upon your personal configuration, you may be
able to rely successfully upon your PATH variable without this step.  Additionally,
you can chose to omit just one of the `--python` or `--sclang` flags if you would
like to provide a path to only one.  Most users with multiple installations of Python
should run this step to ensure that sckernel uses the correct instance of Python.

The typical paths for sclang are as follows but may be different on your machine.

OS X: `"/Applications/SuperCollider/SuperCollider.app/Contents/Resources/sclang"`  
Linux: `"/usr/local/bin/sclang"`  
Windows: `"C:\Program Files\SuperCollider\sclang.exe"`  

## Using SuperCollider kernel

When opening Jupyter notebook, select from the <i>New</i> menu SC_Kernel to create
a new SuperCollider notebook using sclang.

For the console frontend, you can run `jupyter console --kernel sckernel`.

## Converting from Notebooks to SuperCollider files (.scd)

The sckernel package also comes with a convenience script to translate
from Jupyter notebooks to .scd files (i.e., SuperCollider files).  

```
python -m sckernel.convertNotebookToScd /path/to/notebook /path/to/destination
```

Some light formatting is done to make the .scd files readable in a similar way
to Jupyter Notebooks.

## Version Log

### 0.3.0

- Created a configuration file for sckernel to read paths to python and sclang
  to support different installations
- Reorganized sclangSub.py
- Updated documentation to reflect the need for running sckernel.config

### 0.2.0

- Eliminated window flicker on MacOS
- Added syntax highlighting by implementing CodeMirror

### 0.1.0

- First version of sckernel
