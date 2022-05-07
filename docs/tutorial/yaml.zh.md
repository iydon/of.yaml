测试

## Why use YAML

Using YAML to describe OpenFOAM cases will make it easy to modify case parameters, thanks to the popularity of YAML (Python has the [PyYAML](https://github.com/yaml/pyyaml) library, for example). When we need to generate cases on a large scale, we can prepare a template as needed and then use the interface library to keep modifying the case parameters.



## File Structure

### [OpenFOAM Case](https://www.openfoam.com/documentation/user-guide/2-openfoam-cases/2.1-file-structure-of-openfoam-cases)

The basic directory structure for a OpenFOAM case, that contains the minimum set of files required to run an application, is shown in Figure 2.1 and described as follows:

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


### YAML Configuration

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

The YAML file is divided into four main blocks (which can be added as needed):

- 1st block is fixed to the meta block that records case meta information, version number, and the name of each block of the YAML file. It is worth noting that neither forward nor backward compatibility is supported until the specification is stable;

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

- 2nd block is the foam block for recording OpenFOAM case files. In order to retain files in arbitrarily deep directories, this block uses a recursive dictionary to store data. The dictionary is treated as a separate file only if it contains the key `FoamFile`, and all keys indexed to that file correspond to the directory in which it is located;

```yaml
# the way it is written when it first appears
FoamFile: &FoamFile
    version: 2.0
    format: ascii
    class: ...
    object: ...
# the way it is written the rest of the time
FoamFile:
    class: ...
    object: ...
    <<: *FoamFile
```

- 3rd block is the static file block, which is used to record other static files that are not part of the OpenFOAM case specification. This block stores the data as a list, each element of which contains the keys for `name`, `type`, `permission` and `data`;

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

- 4th block is used to store data for which no category has been thought of yet, and currently this block has pipeline (equivalent to `Allrun`).

```yaml
---  # other
pipeline:
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
