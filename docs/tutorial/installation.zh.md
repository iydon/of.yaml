## 先决条件（Prerequisites）

- 支持 **[OpenFOAM](https://github.com/OpenFOAM)** 的操作系统；
- **[Python](https://www.python.org/downloads/)** 3.7 或更高版本。



## 选项 1：通过 `pip` 安装

本项目以 `ifoam` 的名称发布在 [PyPI](https://pypi.python.org/pypi/ifoam) 上，您可以通过 `pip` 软件包管理器从 PyPI 镜像轻松安装。注意，您必须使用 Python 3 版本的 `pip`。

- 如果您需要操作 7z 文件的话，需要额外指定选项 `7z`；
- 如果您需要命令行转化工具的话，需要额外指定选项 `cli`；
- 如果您需要进度条辅助的话，需要额外指定选项 `tqdm`；
- 如果您需要对案例进行后处理的话，需要额外指定选项 `vtk`；
- 如果您以上所有特性都需要的话，可以统一指定选项 `full`；

```shell
$ pip3 install ifoam[7z]
$ pip3 install ifoam[7z,tqdm,vtk]
$ pip3 install ifoam[full]
```



## 选项 2：通过 `poetry` 安装

目前本项目使用 [Poetry](https://github.com/python-poetry/poetry) 来管理 Python 库的依赖，安装方面可以参考[官方安装指南](https://github.com/python-poetry/poetry#installation)。最近我听说 [PDM](https://github.com/pdm-project/pdm) 不错，后续可能会尝试该工具。

1. 克隆本项目
    ```shell
    $ git clone https://github.com/iydon/of.yaml.git
    ```
2. 安装 Python 依赖
    ```shell
    $ poetry install --extras "7z"
    $ poetry install --extras "7z tqdm vtk"
    $ poetry install --extras "full"
    ```
3. 激活虚拟环境
   ```shell
   $ poetry shell
   ```



## 选项 3：通过本项目的 standalone 版本

本选项依赖于选项 2，在安装完 Python 依赖的虚拟环境下运行 `make standalone` 命令，该命令产出的 `foam.py` 文件基本等价于 `foam` 文件夹代表的库，只不过在使用时需要额外注意该库的导入方式。当然，该有的 Python 依赖还是需要安装的，具体参考如下配置信息。

```yaml
PyYAML = { version = "^6.0", optional = false }
py7zr = { version = "^0.17.2", optional = true }
click = { version = "^8.0.3", optional = true }
tqdm = { version = "^4.63.1", optional = true }
vtk = { version = "^9.1.0", optional = true }
```
