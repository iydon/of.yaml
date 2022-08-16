## 示例代码

让我们在 [IPython](https://github.com/ipython/ipython) 中运行示例代码（IPython 不包括在虚拟环境的 Python 依赖中），在逐行输入后我们将得到如下结果。如结果所示，获取 OpenFOAM 与算例的各类信息、修改案例参数并运行案例、直观感受运行时的进度信息与对运行结果进行后处理的功能均完美运行。

```python
In [1]: from foam import Foam

In [2]: # core

In [3]: foam = Foam.from_file('tutorials/incompressible/simpleFoam/airFoil2D.yaml')

In [4]: foam.meta
Out[4]:
{'openfoam': [7],
 'version': '0.7.0',
 'order': ['meta', 'foam', 'static', 'other']}

In [5]: foam['foam']['system', 'controlDict', 'endTime'] = 365

In [6]: foam['foam']['system', 'controlDict']
Out[6]:
{'FoamFile': {'version': 2.0,
  'format': 'ascii',
  'class': 'dictionary',
  'object': 'controlDict'},
 'application': 'simpleFoam',
 'startFrom': 'startTime',
 'startTime': 0,
 'stopAt': 'endTime',
 'endTime': 365,
 'deltaT': 1,
 'writeControl': 'timeStep',
 'writeInterval': 50,
 'purgeWrite': 0,
 'writeFormat': 'ascii',
 'writePrecision': 6,
 'writeCompression': False,
 'timeFormat': 'general',
 'timePrecision': 6,
 'runTimeModifiable': True}

In [7]: foam.save('airFoil2D')
Out[7]: <Foam @ ".../tutorials/incompressible/simpleFoam">

In [8]: # info

In [9]: targets = ('fvSchemes', 'divSchemes', 'div(rhoPhi, U)')

In [10]: print(foam.info.search(*targets))
{'Gauss linearUpwind grad(U);', 'Gauss linearUpwindV grad(U);', 'Gauss LUST grad(U);', 'Gauss upwind;', 'Gauss limitedLinearV 1;', 'Gauss vanLeerV;', 'Gauss linear;'}

In [11]: print(set(foam.info.search_yaml(*targets)))
{'Gauss vanLeerV', 'Gauss LUST grad(U)', 'Gauss limitedLinearV 1', 'Gauss limitedLinearV 1;', 'Gauss linear', 'Gauss upwind', 'Gauss linearUpwind grad(U)'}

In [12]: codes = foam.cmd.all_run()
    ...: assert all(code==0 for code in codes)
Running simpleFoam on /mnt/d/Desktop/GitHub/of.yaml/airFoil2D using 1 processes if in parallel
 86%|████████████████████████████████████████████████████▎        | 313.0/365.0 [00:09<00:01, 32.95it/s]

In [14]: # vtks

In [15]: for time, vtk in zip(foam.cmd.times, foam.post.vtks):
    ...:     print(time, vtk.centroid('p'))
    ...:
Running postProcess on /mnt/d/Desktop/GitHub/of.yaml/airFoil2D using 1 processes if in parallel
 86%|███████████████████████████████████████████████████▍        | 313.0/365.0 [00:02<00:00, 137.61it/s]
 Running postProcess on /mnt/d/Desktop/GitHub/of.yaml/airFoil2D using 1 processes if in parallel
 86%|███████████████████████████████████████████████████▍        | 313.0/365.0 [00:01<00:00, 166.93it/s]
 Running foamToVTK on /mnt/d/Desktop/GitHub/of.yaml/airFoil2D using 1 processes if in parallel
 86%|████████████████████████████████████████████████████▎        | 313.0/365.0 [00:03<00:00, 87.20it/s]
  0.0 [nan nan nan]
 50.0 [-1.4844278e+02 -1.3489431e+03  2.5000008e-02]
100.0 [ 2.7128292e+01 -9.4044006e+02  2.5000006e-02]
150.0 [ 3.8805740e+01 -9.2829706e+02  2.4999999e-02]
200.0 [ 4.135056e+01 -9.269988e+02  2.500000e-02]
250.0 [ 4.1970356e+01 -9.2516913e+02  2.5000000e-02]
300.0 [ 4.2135693e+01 -9.2471173e+02  2.4999993e-02]
313.0 [ 4.2152706e+01 -9.2465576e+02  2.5000002e-02]
```



## [pydoc](https://docs.python.org/3/library/pydoc.html) 文档
```
Help on package foam:

NAME
    foam - Convert multiple dictionary type data to OpenFOAM test case

DESCRIPTION
    Example:
        >>> foam = Foam.from_file('tutorials/incompressible/simpleFoam/airFoil2D.yaml')
        >>> foam['foam']['system', 'controlDict', 'endTime'] = 700
        >>> foam.save('airFoil2D')
        >>> foam.cmd.all_run()

PACKAGE CONTENTS
    __main__
    app (package)
    base (package)

CLASSES
    builtins.object
        foam.base.core.Foam

    class Foam(builtins.object)
     |  Foam(data: List[Dict[str, Any]], root: Union[str, pathlib.Path]) -> None
     |
     |  Convert multiple dictionary type data to OpenFOAM test case
     |
     |  Example:
     |      >>> foam = Foam.from_file('tutorials/incompressible/simpleFoam/airFoil2D.yaml')
     |      >>> foam['foam']['system', 'controlDict', 'endTime'] = 700
     |      >>> foam.save('airFoil2D')
     |      >>> foam.cmd.all_run()
     |
     |  Methods defined here:
     |
     |  __getitem__(self, key: str) -> Union[ForwardRef('Data'), NoneType]
     |
     |  __init__(self, data: List[Dict[str, Any]], root: Union[str, pathlib.Path]) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  __repr__(self) -> str
     |      Return repr(self).
     |
     |  application = <functools.cached_property object>
     |  environ = <functools.cached_property object>
     |  fields = <functools.cached_property object>
     |  ndim = <functools.cached_property object>
     |  number_of_processors = <functools.cached_property object>
     |  pipeline = <functools.cached_property object>
     |  reset(self) -> 'Foam'
     |
     |  save(self, dest: Union[str, pathlib.Path], paraview: bool = True) -> 'Foam'
     |      Persist case to hard disk
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  as_placeholder() -> 'Foam' from builtins.type
     |
     |  from_file(path: Union[str, pathlib.Path]) -> 'Foam' from builtins.type
     |      Supported format: json, yaml
     |
     |  from_json(text: str, root: Union[str, pathlib.Path]) -> 'Foam' from builtins.type
     |
     |  from_yaml(text: str, root: Union[str, pathlib.Path]) -> 'Foam' from builtins.type
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  cmd
     |      `app.command.Command`
     |
     |  info
     |      `app.information.Information`
     |
     |  meta
     |      Meta information
     |
     |  post
     |      `app.postprocess.PostProcess`
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  Self = 'Foam'
     |
     |  parse = <foam.base.parse.Parser object>

DATA
    __all__ = ['app', 'Foam']

VERSION
    0.10.2
```
