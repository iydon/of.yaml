## 示例代码

让我们在 [IPython](https://github.com/ipython/ipython) 中运行示例代码（IPython 不包括在虚拟环境的 Python 依赖中），在逐行输入后我们将得到如下结果。如结果所示，获取 OpenFOAM 与算例的各类信息、修改案例参数并运行案例、直观感受运行时的进度信息与对运行结果进行后处理的功能均完美运行。

```python
In [1]: from foam import Foam

In [2]: # core

In [3]: foam = Foam.from_file('extra/tutorial/tutorials/7/incompressible/simpleFoam/airFoil2D.yaml')

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
        >>> foam = Foam.from_remote_demo('cavity')
        >>> foam['foam']['system', 'controlDict', 'endTime'] = 1.0
        >>> foam.save('cavity')
        >>> foam.cmd.all_run()

PACKAGE CONTENTS
    __main__
    app (package)
    base (package)
    compat (package)
    namespace
    parse (package)
    util (package)

SUBMODULES
    _compat

CLASSES
    abc.ABC(builtins.object)
        foam.util.object.case.CaseBase
    builtins.object
        foam.app.command.core.Command
        foam.app.information.core.Information
        foam.app.postprocess.core.PostProcess
        foam.app.postprocess.core.VTK
        foam.base.core.Foam
        foam.util.object.data.Data
        foam.util.object.email.Envelope
        foam.util.object.email.SMTP
        foam.util.object.figure.Figure
        foam.util.object.timer.Timer
    builtins.tuple(builtins.object)
        foam.util.object.version.Version

    class CaseBase(abc.ABC)
     |  CaseBase(**kwargs: Any) -> None
     |
     |  Case abstract class
     |
     |  Example:
     |      ```
     |      class CaseCavity(CaseBase):
     |          __template__ = 'foam/static/demo/7/cavity.yaml'
     |
     |          @property
     |          def t(self) -> float:
     |              return self._required['t']
     |
     |          def optional(self):
     |              pass
     |
     |          def required(self, t: float, dt: float):
     |              return self.dict_without_keys(vars(), 'self')
     |
     |          def finalize(self, foam, optional, required):
     |              foam['foam'].set_via_dict({
     |                  'system': {
     |                      'controlDict': {
     |                          'endTime': self.t,
     |                          'deltaT': required['dt'],
     |                      },
     |                  },
     |              })
     |      ```
     |
     |      >>> case_template = CaseCavity.new(t=0.3, dt=0.005)
     |      >>> print(case_template)
     |      CaseCavity(t=0.3, dt=0.005) \
     |          .set_optional() \
     |          .set_optional(t=0.3, dt=0.005)
     |      >>> for t in [0.3, 0.4, 0.5]:
     |      ...     parts = 'case', str(t)
     |      ...     case = case_template \
     |      ...         .copy(deepcopy=False) \
     |      ...         .set_required(t=t) \
     |      ...         .save(*parts)
     |      ...     case.parameter.dump_to_path(*parts, 'meta.json')
     |      ...     codes = case.foam.cmd.all_run(overwrite=False)
     |      ...     print(codes)
     |      [0, 0]
     |      [0, 0]
     |      [0, 0]
     |
     |  Method resolution order:
     |      CaseBase
     |      abc.ABC
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__(self, **kwargs: Any) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  __repr__(self) -> str
     |      Return repr(self).
     |
     |  copy(self, deepcopy: bool = False) -> 'Self'
     |
     |  finalize(self, foam: 'Foam', optional: Dict[str, Any], required: Dict[str, Any]) -> Union[ForwardRef('Foam'), NoneType]
     |      Convert class properties to case parameters
     |
     |  optional(self) -> Union[Dict[str, Any], NoneType]
     |      Initialize optional properties
     |
     |  required(self, **kwargs: Any) -> Union[Dict[str, Any], NoneType]
     |      Initialize required properties
     |
     |  save(self, *parts: str) -> 'Self'
     |
     |  set_from_path(self, *parts: str) -> 'Self'
     |
     |  set_optional(self, **kwargs: Any) -> 'Self'
     |
     |  set_required(self, **kwargs: Any) -> 'Self'
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  new(**kwargs: Any) -> 'Self' from abc.ABCMeta
     |
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |
     |  dict_without_keys(data: dict, *keys: str) -> dict
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  data
     |
     |  foam
     |
     |  parameter
     |
     |  tempalte
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
     |  __abstractmethods__ = frozenset({'finalize', 'optional', 'required'})
     |
     |  __template__ = None

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
     |  macros = <foam.compat.functools.cached_property object>
     |  raw(self, command: str, output: bool = True) -> subprocess.CompletedProcess
     |      Execute raw command in case directory
     |
     |  run(self, commands: List[Union[str, Dict[str, Any]]], suffix: str = '', overwrite: bool = False, exception: bool = True, parallel: bool = True, unsafe: bool = False) -> List[int]
     |      Inspired by `runApplication` and `runParallel`
     |
     |      - Reference:
     |          - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/tools/RunFunctions
     |
     |  which(self, command: str) -> Union[str, NoneType]
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  from_foam(foam: 'Foam') -> 'Self' from builtins.type
     |
     |  from_foam_without_asserting(foam: 'Foam') -> 'Self' from builtins.type
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

    class Data(builtins.object)
     |  Data(data: Union[Dict[str, Any], List[Any]]) -> None
     |
     |  Multi-key dictionary
     |
     |  Example:
     |      >>> data = Data.from_dict_keys(
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
     |  dump(self, *paths: Union[str, pathlib.Path]) -> 'Self'
     |
     |  dump_to_path(self, *parts: str) -> 'Self'
     |
     |  dumps(self, type: str = 'yaml', **kwargs: Any) -> bytes
     |
     |  get(self, key: Any, default: Union[Any, NoneType] = None) -> Any
     |
     |  items(self, with_list: bool = False) -> Iterator[Tuple[Union[Any, Tuple[Any, ...]], Any]]
     |
     |  set_default(self, *keys: Any, default: Any = None) -> 'Self'
     |
     |  set_via_dict(self, data: Dict[str, Any]) -> 'Self'
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  from_any(data: Union[Dict[str, Any], List[Any]]) -> 'Self' from builtins.type
     |
     |  from_dict(data: Union[Dict[str, Any], NoneType] = None) -> 'Self' from builtins.type
     |
     |  from_dict_keys(*keys: Hashable, default: Callable = <class 'dict'>) -> 'Self' from builtins.type
     |
     |  from_list(data: Union[List[Any], NoneType] = None) -> 'Self' from builtins.type
     |
     |  from_list_length(length: int, default: Callable = <function Data.<lambda> at 0x7f5242eae940>) -> 'Self' from builtins.type
     |
     |  load(*paths: Union[str, pathlib.Path]) -> Iterator[ForwardRef('Self')] from builtins.type
     |
     |  load_from_path(*parts: str) -> 'Self' from builtins.type
     |
     |  loads(content: bytes, type: str = 'yaml') -> 'Self' from builtins.type
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

    class Envelope(builtins.object)
     |  Envelope(*to_addresses: str) -> None
     |
     |  Envelope
     |
     |  Reference:
     |      - https://github.com/tomekwojcik/envelopes
     |
     |  Methods defined here:
     |
     |  __init__(self, *to_addresses: str) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  add_attachment(self, path: Union[str, pathlib.Path], type: Union[str, NoneType] = None, **kwargs: Any) -> 'Self'
     |      Reference:
     |          - https://docs.python.org/zh-cn/3/library/email.examples.html
     |
     |  send(self) -> None
     |
     |  send_by(self, *smtps: 'SMTP') -> 'Self'
     |
     |  set(self, **kwargs: str) -> 'Self'
     |
     |  set_content(self, value: str, html: bool = False) -> 'Self'
     |
     |  set_content_by_path(self, value: Union[str, pathlib.Path], html: bool = False) -> 'Self'
     |
     |  set_date(self, value: Union[float, NoneType]) -> 'Self'
     |
     |  set_subject(self, value: str) -> 'Self'
     |
     |  to_message(self) -> 'EmailMessage'
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  auto(smtp: 'SMTP') -> 'Self' from builtins.type
     |      Auto-delivered envelope
     |
     |  to(*addresses: str) -> 'Self' from builtins.type
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

    class Figure(builtins.object)
     |  Figure(**kwargs: Any) -> None
     |
     |  Matplotlib simple wrapper
     |
     |  Example:
     |      >>> Figure.new(figsize=(4, 3)) \
     |      ...     .plot([1, 2, 3], [3, 2, 1], label='a') \
     |      ...     .plot([1, 2, 3], [2, 1, 3], label='b') \
     |      ...     .set(xlabel='x label', ylabel='y label', title='title') \
     |      ...     .grid() \
     |      ...     .legend() \
     |      ...     .save('demo.png')
     |      <foam.util.object.figure.Figure at ...>
     |
     |  Methods defined here:
     |
     |  __init__(self, **kwargs: Any) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  grid(self, *args: Any, **kwargs: Any) -> 'Self'
     |
     |  legend(self, *args: Any, **kwargs: Any) -> 'Self'
     |
     |  plot(self, *args: Any, **kwargs: Any) -> 'Self'
     |
     |  save(self, path: Union[str, pathlib.Path], **kwargs: Any) -> 'Self'
     |
     |  set(self, *args: Any, **kwargs: Any) -> 'Self'
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  new(**kwargs: Any) -> 'Self' from builtins.type
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
     |  __annotations__ = {'_ax': '_axes.SubplotBase', '_fig': '_figure.Figure...

    class Foam(builtins.object)
     |  Foam(data: List[Union[Dict[str, Any], List[Any]]], root: Union[str, pathlib.Path], warn: bool = True) -> None
     |
     |  Convert multiple dictionary type data to OpenFOAM test case
     |
     |  Example:
     |      >>> foam = Foam.from_remote_demo('cavity')
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
     |  application = <foam.compat.functools.cached_property object>
     |  copy(self) -> 'Self'
     |
     |  environ = <foam.compat.functools.cached_property object>
     |  fields = <foam.compat.functools.cached_property object>
     |  ndim = <foam.compat.functools.cached_property object>
     |  number_of_processors = <foam.compat.functools.cached_property object>
     |  pipeline = <foam.compat.functools.cached_property object>
     |  reset(self) -> 'Self'
     |
     |  save(self, dest: Union[str, pathlib.Path], paraview: bool = True) -> 'Self'
     |      Persist case to hard disk
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  as_placeholder() -> 'Self' from builtins.type
     |
     |  from_demo(name: str = 'cavity', warn: bool = False) -> 'Self' from builtins.type
     |
     |  from_demos(warn: bool = False) -> List[ForwardRef('Self')] from builtins.type
     |
     |  from_json(text: str, root: Union[str, pathlib.Path], warn: bool = True) -> 'Self' from builtins.type
     |
     |  from_openfoam(path: Union[str, pathlib.Path], **kwargs: Any) -> 'Self' from builtins.type
     |      From OpenFOAM directory
     |
     |  from_path(path: Union[str, pathlib.Path], warn: bool = True) -> 'Self' from builtins.type
     |      Supported path mode: file, directory
     |
     |  from_remote_demo(name: str = 'cavity', timeout: Union[float, NoneType] = None, warn: bool = False) -> 'Self' from builtins.type
     |
     |  from_remote_demos(timeout: Union[float, NoneType] = None, warn: bool = False) -> List[ForwardRef('Self')] from builtins.type
     |
     |  from_remote_path(url: str, timeout: Union[float, NoneType] = None, warn: bool = True) -> 'Self' from builtins.type
     |
     |  from_text(text: str, root: Union[str, pathlib.Path], suffix: Union[str, NoneType] = None, warn: bool = True) -> 'Self' from builtins.type
     |      Supported format: json, yaml
     |
     |  from_yaml(text: str, root: Union[str, pathlib.Path], warn: bool = True) -> 'Self' from builtins.type
     |
     |  list_demos() -> List[str] from builtins.type
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
     |      - Reference:
     |          - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/bin/foamSearch
     |          - https://github.com/OpenFOAM/OpenFOAM-7/blob/master/applications/utilities/miscellaneous/foamDictionary/foamDictionary.C
     |
     |  search_yaml(self, *targets: str, root: Union[str, pathlib.Path] = '.') -> Dict[Hashable, Set[str]]
     |      `foamSearch` in YAML
     |
     |      - Note:
     |          - `targets` should be as detailed as possible, as it is assumed that `targets` will only appear once in a file
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  from_foam(foam: 'Foam') -> 'Self' from builtins.type
     |
     |  from_nothing() -> 'Self' from builtins.type
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
     |  from_foam(foam: 'Foam') -> 'Self' from builtins.type
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  logs
     |      Script extract data for each time-step from a log file for graphing
     |
     |      - Reference:
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

    class SMTP(builtins.object)
     |  SMTP(domain: str, host: str, port: int, ssl: bool = True) -> None
     |
     |  SMTP wrapper
     |
     |  Example:
     |      >>> with SMTP.aio('163', username, password, ssl=False) as smtp:
     |      ...     smtp.envelope \
     |      ...         .to('liangiydon@gmail.com') \
     |      ...         .set_subject('SMTP Test') \
     |      ...         .set_content('Here is the <a href="http://www.python.org">link</a> you wanted.', html=True) \
     |      ...         .add_attachment(__file__) \
     |      ...         .send()
     |
     |  Methods defined here:
     |
     |  __enter__(self) -> 'Self'
     |
     |  __exit__(self, type, value, traceback) -> None
     |
     |  __init__(self, domain: str, host: str, port: int, ssl: bool = True) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  login(self, username: str, password: str) -> 'Self'
     |
     |  quit(self) -> None
     |
     |  send(self, *envelopes: 'Envelope') -> 'Self'
     |
     |  wait(self, seconds: float) -> 'Self'
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  __class_getitem__(key: str) -> 'Self' from builtins.type
     |
     |  aio(mail: str, username: str, password: str, ssl: bool = True) -> 'Self' from builtins.type
     |      All-in-one
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  envelope
     |
     |  sender
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

    class Timer(builtins.object)
     |  Timer(func: Callable) -> None
     |
     |  Timer
     |
     |  Example:
     |      >>> timer = Timer.default()
     |      >>> with timer.new('1', '2', '3') as t:
     |      ...     time.sleep(9)
     |      >>> print(float(t), timer['1', '2', '3'])
     |      9.00686868999037 9.00686868999037
     |
     |  Reference:
     |      - https://docs.python.org/3/library/time.html
     |      - https://stackoverflow.com/questions/5849800/what-is-the-python-equivalent-of-matlabs-tic-and-toc-functions
     |
     |  Methods defined here:
     |
     |  __enter__(self) -> 'Self'
     |
     |  __exit__(self, type, value, traceback) -> None
     |
     |  __getitem__(self, labels: Union[Hashable, Tuple[Hashable, ...]]) -> float
     |
     |  __init__(self, func: Callable) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  __repr__(self) -> str
     |      Return repr(self).
     |
     |  __str__(self) -> str
     |      Return str(self).
     |
     |  new(self, *labels: Hashable, builtin: bool = False) -> Iterator[ForwardRef('TimerResult')]
     |
     |  reset(self) -> 'Self'
     |
     |  wait(self, seconds: float) -> 'Self'
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  best() -> 'Self' from builtins.type
     |
     |  default() -> 'Self' from builtins.type
     |
     |  monotonic() -> 'Self' from builtins.type
     |      Return the value (in fractional seconds) of a monotonic clock, i.e. a clock that cannot go backwards. The clock is not affected by system clock updates. The reference point of the returned value is undefined, so that only the difference between the results of two calls is valid.
     |
     |  perf_counter() -> 'Self' from builtins.type
     |      Return the value (in fractional seconds) of a performance counter, i.e. a clock with the highest available resolution to measure a short duration. It does include time elapsed during sleep and is system-wide. The reference point of the returned value is undefined, so that only the difference between the results of two calls is valid.
     |
     |  process_time() -> 'Self' from builtins.type
     |      Return the value (in fractional seconds) of the sum of the system and user CPU time of the current process. It does not include time elapsed during sleep. It is process-wide by definition. The reference point of the returned value is undefined, so that only the difference between the results of two calls is valid.
     |
     |  thread_time() -> 'Self' from builtins.type
     |      Return the value (in fractional seconds) of the sum of the system and user CPU time of the current thread. It does not include time elapsed during sleep. It is thread-specific by definition. The reference point of the returned value is undefined, so that only the difference between the results of two calls in the same thread is valid.
     |
     |  time() -> 'Self' from builtins.type
     |      Return the time in seconds since the epoch as a floating point number. The specific date of the epoch and the handling of leap seconds is platform dependent. On Windows and most Unix systems, the epoch is January 1, 1970, 00:00:00 (UTC) and leap seconds are not counted towards the time in seconds since the epoch. This is commonly referred to as Unix time. To find out what the epoch is on a given platform, look at gmtime(0).
     |
     |      Note that even though the time is always returned as a floating point number, not all systems provide time with a better precision than 1 second. While this function normally returns non-decreasing values, it can return a lower value than a previous call if the system clock has been set back between the two calls.
     |
     |      The number returned by time() may be converted into a more common time format (i.e. year, month, day, hour, etc…) in UTC by passing it to gmtime() function or in local time by passing it to the localtime() function. In both cases a struct_time object is returned, from which the components of the calendar date may be accessed as attributes.
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  cache
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
     |      - Reference:
     |          - https://github.com/OpenFOAM/OpenFOAM-7/tree/master/src/sampling/probes
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  from_file(path: Union[str, pathlib.Path], **kwargs: Any) -> 'Self' from builtins.type
     |
     |  from_foam(foam: 'Foam', options: str = '', overwrite: bool = False, **kwargs: Any) -> Iterator[ForwardRef('Self')] from builtins.type
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
     |      >>> version = Version.from_string('1.2.x')
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
     |  from_string(version: str) -> 'Self' from builtins.type
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
    __all__ = ['Command', 'Information', 'PostProcess', 'VTK', 'Foam', 'Ca...
    __license__ = 'GPL-3.0-only'

VERSION
    0.12.5
```
