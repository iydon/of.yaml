## 为什么使用 YAML 格式

由于 YAML 是通用配置文件格式，并且主流编程语言均有工具可以解析该配置文件格式，虽然长篇缩进可能让人迷惑（此时可以借助编辑器的功能减轻部分迷惑），但是 YAML 格式的内容更为紧凑，较 JSON 与 TOML 更便于手写。当您需要大规模生成案例时，可以首先根据需要准备一个 YAML 模板，之后借助本项目不断地修改案例参数，生成对应的 OpenFOAM 案例。



## 文件结构

### [OpenFOAM 案例](https://www.openfoam.com/documentation/user-guide/2-openfoam-cases/2.1-file-structure-of-openfoam-cases)

最小 OpenFOAM 案例的基本目录结构如下，其中 `constant/polyMesh` 目录可以由 `system/blockMeshDict` 文件借助 `blockMesh` 命令自动生成。

```
📁 <case>
├── 📁 constant
│    ├── 📁 polyMesh
│    │    ├── boundary
│    │    ├── faces
│    │    ├── neighbour
│    │    ├── owner
│    │    └── points
│    └── properties
├── 📁 system
│    ├── controlDict
│    ├── fvSchemes
│    └── fvSolution
└── 📁 time directories
```


### YAML 配置

```yaml linenums="1" title="airFoil2D.yaml"
---  # meta
...
---  # foam
"0":
    ...
constant:
    ...
system:
    ...
---  # static
...
---  # other
...
```

YAML 配置文件主要分为四个主要子文档（后续可以根据需要拓展）。

- 第 1 个子文档固定记录元（meta）信息，主要包括案例元信息、所需本项目的版本号与 YAML 各子文档的名称。值得注意的是，在 `v1.0` 版本之前，规范并不稳定，既不保证前向兼容也不保证向后兼容；

```yaml
---  # meta
openfoam: [7]
version: 0.7.0
order:
    - meta
    - foam
    - static
    - other
```

- 第 2 个子文档一般记为 `foam`，该部分主要记录符合 OpenFOAM 规范的配置文件信息，它们的统一特征为均包含 `FoamFile` 键。为保留任意深度的文件结构，该部分使用递归字典的方式来存储数据，直到见到 `FoamFile` 键为止；

```yaml
# FoamFile 第一次出现时写作
FoamFile: &FoamFile
    version: 2.0
    format: ascii
    class: <class_name>
    object: <object_name>
# FoamFile 后续出现时写作
FoamFile:
    class: <class_name>
    object: <object_name>
    <<: *FoamFile
# 更新后可以省略 version 与 format 信息
FoamFile:
    class: <class_name>
    object: <object_name>
# 甚至当 object 为文件名时也可以省略
FoamFile: <class_name>
```

- 第 3 个子文档一般记为 `static`，该部分主要记录不符合 OpenFOAM 规范的其他静态文件，该块以列表的方式存储静态文件，每个元素均包含文件名称、类型、权限与数据信息。该部分主要记录对象为 `All*` 等脚本、网格文件等；

```yaml
-
    name: Allrun
    type: [embed, text]  # Foam::_save_static @ https://github.com/iydon/of.yaml/blob/main/foam/core.py
    permission: 777
    data: |
        #!/bin/sh
        cd ${0%/*} || exit 1    # Run from this directory

        # Source tutorial run functions
        . $WM_PROJECT_DIR/bin/tools/RunFunctions

        application=$(getApplication)

        runApplication $application
```

- 第 4 个子文档一般记为 `other`，该部分主要记录尚未想到类别的数据，即大杂烩。目前该部分固定的内容有 `pipeline`，相当于将 `Allrun` 脚本中的命令进行细颗粒度的拆分。

```yaml
---  # other
pipeline:
    -
        command: blockMesh
        parallel: false
    - __app__
```



## Conversion Specification

### FOAM Block

This section needs to map the [basic input/output file format](https://www.openfoam.com/documentation/user-guide/2-openfoam-cases/2-2-basic-inputoutput-file-format) to the YAML file one by one.

#### Dictionaries

OpenFOAM uses dictionaries as the most common means of specifying data. A dictionary is an entity that contains a set of data entries that can be retrieved by the I/O by means of keywords. The keyword entries follow the general format.

=== "OpenFOAM"
    ```
    <keyword>  <dataEntry1> … <dataEntryN>;
    ```
=== "YAML"
    ```yaml
    <keyword>: <dataEntry1> … <dataEntryN>
    ```

Most OpenFOAM data files are themselves dictionaries containing a set of keyword entries. Dictionaries provide the means for organising entries into logical categories and can be specified hierarchically so that any dictionary can itself contain one or more dictionary entries. The format for a dictionary is to specify the dictionary name followed the entries enclosed in curly braces` {}` as follows.

=== "OpenFOAM"
    ```
    <dictionaryName> {
        … keyword entries …
    }
    ```
=== "YAML"
    ```yaml
    <dictionaryName>:
        …
        keyword entries
        …
    ```

#### Lists

OpenFOAM applications contain lists, e.g. a list of vertex coordinates for a mesh description. Lists are commonly found in I/O and have a format of their own in which the entries are contained within round braces `( )`. There is also a choice of format preceeding the round braces:

**Simple**: the keyword is followed immediately by round braces.

=== "OpenFOAM"
    ```
    <listName>
      (
          … entries …
      );
    ```
=== "YAML"
    ```yaml
    <listName>:
        - …
        - entries
        - …
    ```

**Numbered**: the keyword is followed by the number of elements `<n>` in the list.

=== "OpenFOAM"
    ```
    <listName>
    <n>
    (
        … entries …
    );
    ```
=== "YAML"
    ```yaml
    <listName> <n>:
        - …
        - entries
        - …
    ```

**Token identifier**: the keyword is followed by a class name identifier `Label<Type>` where `<Type>` states what the list contains, e.g. for a list of scalar elements is:

=== "OpenFOAM"
    ```
    <listName>
    List<scalar>
    <n>        // optional
    (
        … entries …
    );
    ```
=== "YAML"
    ```yaml
    # TODO
    ```

#### Scalars, Vectors and Tensors

A scalar is a single number represented as such in a data file. A vector is a VectorSpace of rank 1 and dimension 3, and since the number of elements is always fixed to 3, the simple List format is used. Therefore a vector `(1.0, 1.1, 1.2)` is written:

=== "OpenFOAM"
    ```
    (1.0 1.1 1.2)
    ```
=== "YAML"
    ```yaml
    <keyword>: (1.0 1.1 1.2)
    ```

In OpenFOAM, a tensor is a VectorSpace of rank 2 and dimension 3 and therefore the data entries are always fixed to 9 real numbers. Therefore the identity tensor can be written:

=== "OpenFOAM"
    ```
    (
        1 0 0
        0 1 0
        0 0 1
    )
    ```
=== "YAML"
    ```yaml
    <keyword>: (
            1 0 0
            0 1 0
            0 0 1
        )
    ```
