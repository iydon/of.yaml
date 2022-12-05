## 示例代码

让我们在 [IPython](https://github.com/ipython/ipython) 中运行示例代码（IPython 不包括在虚拟环境的 Python 依赖中），在逐行输入后我们将得到如下结果。如结果所示，获取 OpenFOAM 与算例的各类信息、修改案例参数并运行案例、直观感受运行时的进度信息与对运行结果进行后处理的功能均完美运行。

```python
In [1]: from foam import Foam

In [2]: # core

In [3]: foam = Foam.fromPath('extra/tutorial/tutorials/7/incompressible/simpleFoam/airFoil2D.yaml')

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
Out[7]: <Foam @ ".../extra/tutorial/tutorials/7/incompressible/simpleFoam">

In [8]: # info

In [9]: targets = ('fvSchemes', 'divSchemes', 'div(rhoPhi, U)')

In [10]: print(foam.info.search(*targets))
{'Gauss linearUpwind grad(U);', 'Gauss linearUpwindV grad(U);', 'Gauss LUST grad(U);', 'Gauss upwind;', 'Gauss limitedLinearV 1;', 'Gauss vanLeerV;', 'Gauss linear;'}

In [11]: print(set(foam.info.search_yaml(*targets)))
{'Gauss vanLeerV', 'Gauss LUST grad(U)', 'Gauss limitedLinearV 1', 'Gauss limitedLinearV 1;', 'Gauss linear', 'Gauss upwind', 'Gauss linearUpwind grad(U)'}

In [12]: codes = foam.cmd.all_run()
    ...: assert all(code==0 for code in codes)
Running simpleFoam on .../of.yaml/airFoil2D using 1 processes if in parallel
 86%|████████████████████████████████████████████████████▎        | 313.0/365.0 [00:09<00:01, 32.95it/s]

In [14]: # vtks

In [15]: for time, vtk in zip(foam.cmd.times, foam.post.vtks):
    ...:     print(time, vtk.centroid('p'))
    ...:
Running postProcess on .../of.yaml/airFoil2D using 1 processes if in parallel
 86%|███████████████████████████████████████████████████▍        | 313.0/365.0 [00:02<00:00, 137.61it/s]
 Running postProcess on .../of.yaml/airFoil2D using 1 processes if in parallel
 86%|███████████████████████████████████████████████████▍        | 313.0/365.0 [00:01<00:00, 166.93it/s]
 Running foamToVTK on .../of.yaml/airFoil2D using 1 processes if in parallel
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
        >>> foam = Foam.fromRemoteDemo('cavity')
        >>> foam['foam']['system', 'controlDict', 'endTime'] = 1.0
        >>> foam.save('cavity')
        >>> foam.cmd.all_run()

PACKAGE CONTENTS
    __main__
    app (package)
    base (package)
    compat (package)
    namespace (package)
    parse (package)
    util (package)

CLASSES
    builtins.object
        foam.app.command.core.Command
        foam.app.information.core.Information
        foam.app.postprocess.core.PostProcess
        foam.app.postprocess.core.VTK
        foam.base.core.Foam
        foam.util.object.conversion.Conversion
        foam.util.object.data.Data
    builtins.tuple(builtins.object)
        foam.util.object.version.Version

    class Command(builtins.object)
     |  Command(foam: 'Foam') -> None
     |
     |  OpenFOAM command wrapper
     |
     |  Methods defined here:
     |
     |  __init__(self, foam: 'Foam') -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  all_clean(self) -> None
     |      Inspired by `Allclean`
     |
     |  all_run(self, overwrite: bool = False, exception: bool = False, parallel: bool = True, unsafe: bool = True) -> List[int]
     |      Inspired by  `Allrun`
     |
     |  macros = <functools.cached_property object>
     |  raw(self, command: str, output: bool = True) -> subprocess.CompletedProcess
     |      Execute raw command in case directory
     |
     |  run(self, commands: List[Union[str, Dict[str, Any]]], suffix: str = '', overwrite: bool = False, exception: bool = True, parallel: bool = True, unsafe: bool = False) -> List[int]
     |      Inspired by `runApplication` and `runParallel`
     |
     |      Reference:
     |          - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/tools/RunFunctions
     |
     |  which(self, command: str) -> Union[str, NoneType]
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  fromFoam(foam: 'Foam') -> 'Self' from builtins.type
     |
     |  fromFoamWithoutAsserting(foam: 'Foam') -> 'Self' from builtins.type
     |
     |  from_foam = fromFoam(foam: 'Foam') -> 'Self' from builtins.type
     |
     |  from_foam_without_asserting = fromFoamWithoutAsserting(foam: 'Foam') -> 'Self' from builtins.type
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  logs
     |      Log files
     |
     |  times
     |      Time directories
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

    class Conversion(builtins.object)
     |  Conversion(document: Union[Dict[str, Any], List[Any]]) -> None
     |
     |  Conversion between object and bytes/string
     |
     |  Example:
     |      >>> data = {'a': 1, 'b': [2, 3], 'c': {'4': 5}}
     |      >>> print(Conversion.fromDocument(data).to_yaml())
     |      a: 1
     |      b:
     |      - 2
     |      - 3
     |      c:
     |      '4': 5
     |
     |  Methods defined here:
     |
     |  __init__(self, document: Union[Dict[str, Any], List[Any]]) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  to_bytes(self, type_or_suffix: str = 'json', all: bool = False, **kwargs: Any) -> bytes
     |
     |  to_document(self) -> Union[Dict[str, Any], List[Any]]
     |
     |  to_json(self, **kwargs: Any) -> str
     |
     |  to_path(self, path: Union[str, pathlib.Path], all: bool = False, type: Union[str, NoneType] = None, **kwargs: Any) -> pathlib.Path
     |
     |  to_pickle(self, **kwargs: Any) -> bytes
     |
     |  to_string(self, type: str = 'json', all: bool = False, **kwargs: Any) -> str
     |
     |  to_toml(self, **kwargs: Any) -> str
     |
     |  to_yaml(self, all: bool = False, **kwargs: Any) -> str
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  autoFromBytes(content: bytes, all: bool = False) -> 'Self' from builtins.type
     |
     |  autoFromPath(path: Union[str, pathlib.Path], all: bool = False) -> 'Self' from builtins.type
     |
     |  autoFromString(text: str, all: bool = False) -> 'Self' from builtins.type
     |
     |  auto_from_bytes = autoFromBytes(content: bytes, all: bool = False) -> 'Self' from builtins.type
     |
     |  auto_from_path = autoFromPath(path: Union[str, pathlib.Path], all: bool = False) -> 'Self' from builtins.type
     |
     |  auto_from_string = autoFromString(text: str, all: bool = False) -> 'Self' from builtins.type
     |
     |  fromBytes(content: bytes, type_or_suffix: str = 'json', all: bool = False) -> 'Self' from builtins.type
     |
     |  fromDocument(document: Union[Dict[str, Any], List[Any]]) -> 'Self' from builtins.type
     |
     |  fromJSON(text: str) -> 'Self' from builtins.type
     |
     |  fromPath(path: Union[str, pathlib.Path], all: bool = False, type: Union[str, NoneType] = None) -> 'Self' from builtins.type
     |
     |  fromPickle(text: bytes) -> 'Self' from builtins.type
     |
     |  fromString(text: str, type: str = 'json', all: bool = False) -> 'Self' from builtins.type
     |
     |  fromTOML(text: str) -> 'Self' from builtins.type
     |
     |  fromYAML(text: str, all: bool = False) -> 'Self' from builtins.type
     |
     |  from_bytes = fromBytes(content: bytes, type_or_suffix: str = 'json', all: bool = False) -> 'Self' from builtins.type
     |
     |  from_document = fromDocument(document: Union[Dict[str, Any], List[Any]]) -> 'Self' from builtins.type
     |
     |  from_json = fromJSON(text: str) -> 'Self' from builtins.type
     |
     |  from_path = fromPath(path: Union[str, pathlib.Path], all: bool = False, type: Union[str, NoneType] = None) -> 'Self' from builtins.type
     |
     |  from_pickle = fromPickle(text: bytes) -> 'Self' from builtins.type
     |
     |  from_string = fromString(text: str, type: str = 'json', all: bool = False) -> 'Self' from builtins.type
     |
     |  from_toml = fromTOML(text: str) -> 'Self' from builtins.type
     |
     |  from_yaml = fromYAML(text: str, all: bool = False) -> 'Self' from builtins.type
     |
     |  suffixes(dot: bool = True) -> Set[str] from builtins.type
     |
     |  typeFromSuffix(type_or_suffix: str) -> str from builtins.type
     |
     |  type_from_suffix = typeFromSuffix(type_or_suffix: str) -> str from builtins.type
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

    class Data(builtins.object)
     |  Data(data: Union[Dict[str, Any], List[Any]]) -> None
     |
     |  Multi-key dictionary or list (not recommended)
     |
     |  Example:
     |      >>> data = Data.fromDictKeys(
     |      ...     ('left', 'x'), ('left', 'y'),
     |      ...     ('right', 'x'), ('right', 'y'),
     |      ...     default=list,
     |      ... )
     |      >>> data['left', 'x'].append({...})
     |      >>> data['right', 'y'].append({...})
     |
     |      >>> for key, val in data.items():
     |      ...     print(key, val)
     |      ('left', 'x') [{Ellipsis}]
     |      ('left', 'y') []
     |      ('right', 'x') []
     |      ('right', 'y') [{Ellipsis}]
     |
     |  Methods defined here:
     |
     |  __bool__(self) -> bool
     |
     |  __contains__(self, keys: Union[Any, Tuple[Any, ...]]) -> bool
     |
     |  __getitem__(self, keys: Union[Any, Tuple[Any, ...]]) -> Any
     |
     |  __init__(self, data: Union[Dict[str, Any], List[Any]]) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  __iter__(self) -> Iterator[Any]
     |
     |  __len__(self) -> int
     |
     |  __repr__(self) -> str
     |      Return repr(self).
     |
     |  __setitem__(self, keys: Union[Any, Tuple[Any, ...]], value: Any) -> None
     |
     |  __str__(self) -> str
     |      Return str(self).
     |
     |  contains(self, *keys: Any) -> bool
     |
     |  dump(self, *paths: Union[str, pathlib.Path], type: Union[str, NoneType] = None) -> 'Self'
     |
     |  dump_to_path(self, *parts: str, type: Union[str, NoneType] = None) -> 'Self'
     |
     |  dumps(self, type_or_suffix: str = 'yaml', **kwargs: Any) -> bytes
     |
     |  get(self, key: Any, default: Union[Any, NoneType] = None) -> Any
     |
     |  gets(self, *keys: Any, default: Union[Any, NoneType] = None) -> Any
     |
     |  is_dict(self) -> bool
     |
     |  is_list(self) -> bool
     |
     |  is_other(self) -> bool
     |
     |  items(self, with_list: bool = False) -> Iterator[Tuple[Union[Any, Tuple[Any, ...]], Any]]
     |
     |  set_default(self, *keys: Any, default: Union[Any, NoneType] = None) -> 'Self'
     |
     |  set_via_dict(self, data: Dict[str, Any]) -> 'Self'
     |
     |  setdefault(self, key: Any, default: Union[Any, NoneType] = None) -> Any
     |
     |  to_any(self) -> Union[Dict[str, Any], List[Any]]
     |
     |  to_dict(self) -> Dict[str, Any]
     |
     |  to_list(self) -> List[Any]
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  fromAny(data: Union[Dict[str, Any], List[Any]]) -> 'Self' from builtins.type
     |
     |  fromDict(data: Union[Dict[str, Any], NoneType] = None) -> 'Self' from builtins.type
     |
     |  fromDictKeys(*keys: Hashable, default: Callable = <class 'dict'>) -> 'Self' from builtins.type
     |
     |  fromList(data: Union[List[Any], NoneType] = None) -> 'Self' from builtins.type
     |
     |  fromListLength(length: int, default: Callable = <function Data.<lambda> at 0x7f2e2a7a11f0>) -> 'Self' from builtins.type
     |
     |  from_any = fromAny(data: Union[Dict[str, Any], List[Any]]) -> 'Self' from builtins.type
     |
     |  from_dict = fromDict(data: Union[Dict[str, Any], NoneType] = None) -> 'Self' from builtins.type
     |
     |  from_dict_keys = fromDictKeys(*keys: Hashable, default: Callable = <class 'dict'>) -> 'Self' from builtins.type
     |
     |  from_list = fromList(data: Union[List[Any], NoneType] = None) -> 'Self' from builtins.type
     |
     |  from_list_length = fromListLength(length: int, default: Callable = <function Data.<lambda> at 0x7f2e2a7a11f0>) -> 'Self' from builtins.type
     |
     |  load(*paths: Union[str, pathlib.Path], type: Union[str, NoneType] = None) -> Iterator[ForwardRef('Self')] from builtins.type
     |
     |  loadFromPath(*parts: str, type: Union[str, NoneType] = None) -> 'Self' from builtins.type
     |
     |  load_from_path = loadFromPath(*parts: str, type: Union[str, NoneType] = None) -> 'Self' from builtins.type
     |
     |  loads(content: bytes, type_or_suffix: str = 'yaml') -> 'Self' from builtins.type
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  data
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

    class Foam(builtins.object)
     |  Foam(data: List[Union[Dict[str, Any], List[Any]]], root: Union[str, pathlib.Path], warn: bool = True) -> None
     |
     |  Convert multiple dictionary type data to OpenFOAM test case
     |
     |  Example:
     |      >>> foam = Foam.fromRemoteDemo('cavity')
     |      >>> foam['foam']['system', 'controlDict', 'endTime'] = 1.0
     |      >>> foam.save('cavity')
     |      >>> foam.cmd.all_run()
     |
     |  Methods defined here:
     |
     |  __getitem__(self, key: str) -> Union[foam.util.object.data.Data, NoneType]
     |
     |  __init__(self, data: List[Union[Dict[str, Any], List[Any]]], root: Union[str, pathlib.Path], warn: bool = True) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  __repr__(self) -> str
     |      Return repr(self).
     |
     |  __str__(self) -> str
     |      Return str(self).
     |
     |  application = <functools.cached_property object>
     |  copy(self) -> 'Self'
     |
     |  environ = <functools.cached_property object>
     |  fields = <functools.cached_property object>
     |  ndim = <functools.cached_property object>
     |  number_of_processors = <functools.cached_property object>
     |  pipeline = <functools.cached_property object>
     |  reset(self) -> 'Self'
     |
     |  save(self, dest: Union[str, pathlib.Path], paraview: bool = True) -> 'Self'
     |      Persist case to hard disk
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  default() -> 'Self' from builtins.type
     |
     |  fromDemo(name: str = 'cavity', warn: bool = False, verbose: bool = True) -> 'Self' from builtins.type
     |
     |  fromDemos(warn: bool = False, verbose: bool = True) -> List[ForwardRef('Self')] from builtins.type
     |
     |  fromOpenFoam(path: Union[str, pathlib.Path], **kwargs: Any) -> 'Self' from builtins.type
     |      From OpenFOAM directory
     |
     |  fromPath(path: Union[str, pathlib.Path], warn: bool = True, type: Union[str, NoneType] = None) -> 'Self' from builtins.type
     |      Supported path mode: file, directory
     |
     |  fromRemoteDemo(name: str = 'cavity', timeout: Union[float, NoneType] = None, warn: bool = False, verbose: bool = True) -> 'Self' from builtins.type
     |
     |  fromRemoteDemos(timeout: Union[float, NoneType] = None, warn: bool = False, verbose: bool = True) -> List[ForwardRef('Self')] from builtins.type
     |
     |  fromRemotePath(url: str, timeout: Union[float, NoneType] = None, warn: bool = True, type: Union[str, NoneType] = None) -> 'Self' from builtins.type
     |
     |  fromText(text: Union[bytes, str], root: Union[str, pathlib.Path], type_or_suffix: Union[str, NoneType] = None, warn: bool = True) -> 'Self' from builtins.type
     |      Supported formats: please refer to `Conversion`
     |
     |  fromYAML(text: str, root: Union[str, pathlib.Path], warn: bool = True) -> 'Self' from builtins.type
     |
     |  from_demo = fromDemo(name: str = 'cavity', warn: bool = False, verbose: bool = True) -> 'Self' from builtins.type
     |
     |  from_demos = fromDemos(warn: bool = False, verbose: bool = True) -> List[ForwardRef('Self')] from builtins.type
     |
     |  from_openfoam = fromOpenFoam(path: Union[str, pathlib.Path], **kwargs: Any) -> 'Self' from builtins.type
     |      From OpenFOAM directory
     |
     |  from_path = fromPath(path: Union[str, pathlib.Path], warn: bool = True, type: Union[str, NoneType] = None) -> 'Self' from builtins.type
     |      Supported path mode: file, directory
     |
     |  from_remote_demo = fromRemoteDemo(name: str = 'cavity', timeout: Union[float, NoneType] = None, warn: bool = False, verbose: bool = True) -> 'Self' from builtins.type
     |
     |  from_remote_demos = fromRemoteDemos(timeout: Union[float, NoneType] = None, warn: bool = False, verbose: bool = True) -> List[ForwardRef('Self')] from builtins.type
     |
     |  from_remote_path = fromRemotePath(url: str, timeout: Union[float, NoneType] = None, warn: bool = True, type: Union[str, NoneType] = None) -> 'Self' from builtins.type
     |
     |  from_text = fromText(text: Union[bytes, str], root: Union[str, pathlib.Path], type_or_suffix: Union[str, NoneType] = None, warn: bool = True) -> 'Self' from builtins.type
     |      Supported formats: please refer to `Conversion`
     |
     |  from_yaml = fromYAML(text: str, root: Union[str, pathlib.Path], warn: bool = True) -> 'Self' from builtins.type
     |
     |  listDemos() -> List[str] from builtins.type
     |
     |  list_demos = listDemos() -> List[str] from builtins.type
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  cmd
     |      `app.command.Command`
     |
     |  data
     |
     |  info
     |      `app.information.Information`
     |
     |  meta
     |      Meta information
     |
     |  parser
     |      All parsers
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
     |  destination

    class Information(builtins.object)
     |  Information(foam: 'Foam') -> None
     |
     |  OpenFOAM information wrapper
     |
     |  Methods defined here:
     |
     |  __init__(self, foam: 'Foam') -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  commands(self, foam_only: bool = True) -> Set[str]
     |
     |  search(self, *targets: str, process: bool = True) -> Union[str, Set[str]]
     |      `foamSearch` wrapper
     |
     |      Reference:
     |          - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/foamSearch
     |          - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/miscellaneous/foamDictionary/foamDictionary.C
     |
     |  search_path(self, *targets: str, root: Union[str, pathlib.Path] = '.', suffixes: Union[Set[str], NoneType] = None) -> Dict[Hashable, Set[str]]
     |      `foamSearch` in configuration
     |
     |  search_yaml(self, *targets: str, root: Union[str, pathlib.Path] = '.') -> Dict[Hashable, Set[str]]
     |      `foamSearch` in YAML
     |
     |      Note:
     |          - `targets` should be as detailed as possible, as it is assumed that `targets` will only appear once in a file
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  default() -> 'Self' from builtins.type
     |
     |  fromFoam(foam: 'Foam') -> 'Self' from builtins.type
     |
     |  from_foam = fromFoam(foam: 'Foam') -> 'Self' from builtins.type
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  cmd
     |      Command without asserting (no need to call `Foam::save` method first)
     |
     |  environ
     |      OpenFOAM environments (aliase for `Foam::environ` property)
     |
     |  root
     |
     |  shared_libraries
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

    class PostProcess(builtins.object)
     |  PostProcess(foam: 'Foam') -> None
     |
     |  OpenFOAM post-processing
     |
     |  Methods defined here:
     |
     |  __init__(self, foam: 'Foam') -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  centroid(self, key: str, structured: bool = False) -> Dict[float, ForwardRef('_numpy.ndarray')]
     |
     |  centroids(self, keys: Union[Set[str], NoneType] = None, structured: bool = False) -> Dict[str, Dict[float, ForwardRef('_numpy.ndarray')]]
     |
     |  probe(self, location: Tuple[float, float, float], keys: Union[Set[str], NoneType] = None, point: bool = True, func: Union[Callable, NoneType] = None) -> Dict[str, Dict[float, ForwardRef('_numpy.ndarray')]]
     |
     |  probes(self, *locations: Tuple[float, float, float], keys: Union[Set[str], NoneType] = None, point: bool = True, func: Union[Callable, NoneType] = None) -> Dict[Tuple[float, float, float], Dict[str, Dict[float, ForwardRef('_numpy.ndarray')]]]
     |
     |  vtks_set(self, **kwargs: Any) -> List[ForwardRef('VTK')]
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  fromFoam(foam: 'Foam') -> 'Self' from builtins.type
     |
     |  from_foam = fromFoam(foam: 'Foam') -> 'Self' from builtins.type
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  logs
     |      Script extract data for each time-step from a log file for graphing
     |
     |      Reference:
     |          - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/foamLog
     |
     |  vtks
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

    class VTK(builtins.object)
     |  VTK(reader: '_vtkmodules.vtkIOLegacy.vtkDataReader', foam: Union[ForwardRef('Foam'), NoneType] = None, point: bool = True, cell: bool = True) -> None
     |
     |  OpenFOAM VTK post-processing
     |
     |  Methods defined here:
     |
     |  __contains__(self, key: str) -> bool
     |
     |  __getitem__(self, key: str) -> None
     |
     |  __init__(self, reader: '_vtkmodules.vtkIOLegacy.vtkDataReader', foam: Union[ForwardRef('Foam'), NoneType] = None, point: bool = True, cell: bool = True) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  centroid(self, key: str, structured: bool = False) -> '_numpy.ndarray'
     |
     |  centroid_with_args(self, *keys: str, structured: bool = False) -> Dict[str, ForwardRef('_numpy.ndarray')]
     |
     |  centroids(self, keys: Union[Set[str], NoneType] = None, structured: bool = False) -> Dict[str, ForwardRef('_numpy.ndarray')]
     |
     |  keys(self) -> None
     |
     |  probe(self, location: Tuple[float, float, float], keys: Union[Set[str], NoneType] = None, point: bool = True, func: Union[Callable, NoneType] = None) -> Dict[str, ForwardRef('_numpy.ndarray')]
     |
     |  probes(self, *locations: Tuple[float, float, float], keys: Union[Set[str], NoneType] = None, point: bool = True, func: Union[Callable, NoneType] = None) -> Dict[Tuple[float, float, float], Dict[str, ForwardRef('_numpy.ndarray')]]
     |      Reference:
     |          - https://github.com/OpenFOAM/OpenFOAM-7/tree/master/src/sampling/probes
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  fromFoam(foam: 'Foam', options: str = '', overwrite: bool = False, **kwargs: Any) -> Iterator[ForwardRef('Self')] from builtins.type
     |
     |  fromPath(path: Union[str, pathlib.Path], **kwargs: Any) -> 'Self' from builtins.type
     |
     |  from_foam = fromFoam(foam: 'Foam', options: str = '', overwrite: bool = False, **kwargs: Any) -> Iterator[ForwardRef('Self')] from builtins.type
     |
     |  from_path = fromPath(path: Union[str, pathlib.Path], **kwargs: Any) -> 'Self' from builtins.type
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  cell_fields
     |
     |  cells
     |
     |  foam
     |
     |  point_fields
     |
     |  points
     |
     |  x
     |
     |  y
     |
     |  z
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

    class Version(builtins.tuple)
     |  Version(major: int, minor: int, other: Union[str, NoneType])
     |
     |  Version named tuple
     |
     |  Example:
     |      >>> version = Version.fromString('1.2.x')
     |      >>> version.major, version.minor, version.other, version.micro
     |      (1, 2, 'x', None)
     |      >>> version.to_string()
     |      '1.2.x'
     |
     |  Method resolution order:
     |      Version
     |      builtins.tuple
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __getnewargs__(self)
     |      Return self as a plain tuple.  Used by copy and pickle.
     |
     |  __gt__(self, other: 'Self') -> bool
     |      Return self>value.
     |
     |  __lt__(self, other: 'Self') -> bool
     |      Return self<value.
     |
     |  __repr__(self) -> str
     |      Return repr(self).
     |
     |  __str__(self) -> str
     |      Return str(self).
     |
     |  _asdict(self)
     |      Return a new dict which maps field names to their values.
     |
     |  _replace(self, /, **kwds)
     |      Return a new Version object replacing specified fields with new values
     |
     |  to_string(self) -> str
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  _make(iterable) from builtins.type
     |      Make a new Version object from a sequence or iterable
     |
     |  fromString(version: str) -> 'Self' from builtins.type
     |
     |  from_string = fromString(version: str) -> 'Self' from builtins.type
     |
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |
     |  __new__(_cls, major: int, minor: int, other: Union[str, NoneType])
     |      Create new instance of Version(major, minor, other)
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  micro
     |
     |  micro_int
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  major
     |      Alias for field number 0
     |
     |  minor
     |      Alias for field number 1
     |
     |  other
     |      Alias for field number 2
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  __annotations__ = {'major': <class 'int'>, 'minor': <class 'int'>, 'ot...
     |
     |  _field_defaults = {}
     |
     |  _field_types = {'major': <class 'int'>, 'minor': <class 'int'>, 'other...
     |
     |  _fields = ('major', 'minor', 'other')
     |
     |  _fields_defaults = {}
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.tuple:
     |
     |  __add__(self, value, /)
     |      Return self+value.
     |
     |  __contains__(self, key, /)
     |      Return key in self.
     |
     |  __eq__(self, value, /)
     |      Return self==value.
     |
     |  __ge__(self, value, /)
     |      Return self>=value.
     |
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |
     |  __getitem__(self, key, /)
     |      Return self[key].
     |
     |  __hash__(self, /)
     |      Return hash(self).
     |
     |  __iter__(self, /)
     |      Implement iter(self).
     |
     |  __le__(self, value, /)
     |      Return self<=value.
     |
     |  __len__(self, /)
     |      Return len(self).
     |
     |  __mul__(self, value, /)
     |      Return self*value.
     |
     |  __ne__(self, value, /)
     |      Return self!=value.
     |
     |  __rmul__(self, value, /)
     |      Return value*self.
     |
     |  count(self, value, /)
     |      Return number of occurrences of value.
     |
     |  index(self, value, start=0, stop=9223372036854775807, /)
     |      Return first index of value.
     |
     |      Raises ValueError if the value is not present.

FUNCTIONS
    __import__ lambda name

DATA
    __all__ = ['Command', 'Conversion', 'Data', 'Foam', 'Information', 'Po...
    __license__ = 'GPL-3.0-only'

VERSION
    0.13.2
```
