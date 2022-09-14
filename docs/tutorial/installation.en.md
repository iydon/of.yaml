## Prerequisites

- Operating systems that support **[OpenFOAM](https://github.com/OpenFOAM)**;
- **[Python](https://www.python.org/downloads/)** 3.7 or later.



## Option 1: Install via `pip`

This project is distributed on [PyPI](https://pypi.python.org/pypi/ifoam) under the name `ifoam`, and you can easily install it from the PyPI image using the `pip` package manager. Note that you must use the Python 3 version of `pip`.

- If you need to manipulate 7z files, you need to specify the additional option `7z`;
- If you need command line tool, you need to specify the additional option `cli`;
- If you need progress bar assistance, specify the additional option `tqdm`;
- If you need to post-process cases, specify the additional option `vtk`;
- If you need all of the above features, you can specify the option `full` uniformly.

```shell
$ pip3 install ifoam[7z]
$ pip3 install ifoam[7z,tqdm,vtk]
$ pip3 install ifoam[full]
```



## Option 2: Install via `poetry`

Currently this project uses [Poetry](https://github.com/python-poetry/poetry) to manage the dependencies of the Python libraries, for installation you can refer to the [official installation guide](https://github.com/python-poetry/poetry#installation). I've recently heard good things about [PDM](https://github.com/pdm-project/pdm), and I may try that tool later.

1. Clone this repository
    ```shell
    $ git clone https://github.com/iydon/of.yaml.git
    ```
2. Install Python dependencies
    ```shell
    $ poetry install --extras "7z"
    $ poetry install --extras "7z tqdm vtk"
    $ poetry install --extras "full"
    ```
3. Activate virtual environment
   ```shell
   $ poetry shell
   ```



## Option 3: Use standalone version of this repository

This option relies on option 2, which runs the `make standalone` command in a virtual environment with Python dependencies installed, and produces a `foam.py` file that is basically equivalent to the library represented by the `foam` folder, except that you need to pay extra attention to how the library is imported. Of course, there are still Python dependencies that need to be installed, as described in the following configuration information.

```yaml
PyYAML = { version = "^6.0", optional = false }
py7zr = { version = "^0.17.2", optional = true }
click = { version = "^8.0.3", optional = true }
tqdm = { version = "^4.63.1", optional = true }
vtk = { version = "^9.1.0", optional = true }
```
