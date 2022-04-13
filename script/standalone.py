import inspect
import pathlib as p
import re
import textwrap
import typing as t

from foam import Foam
from foam.command import Command, progress
from foam.parse import Parse
from foam.postprocessing import VTK
from foam.type import Dict, List, Path, Data


class show:
    @classmethod
    def source(cls, obj: object) -> str:
        pattern = re.compile(r'from \.[\w\.]* import \w+')
        return pattern.sub('', inspect.getsource(obj))

    @classmethod
    def apps(cls, obj: t.Dict[str, t.Type]) -> str:
        content = ',\n'.join(
            f'{key!r}: {value.__name__}'
            for key, value in obj.items()
        )
        return f'{{\n{cls._indent(content)}\n}}'

    @classmethod
    def code(cls, obj: str) -> str:
        br = '\n'
        pattern = re.compile(fr'{br}{{3,}}')
        lines = obj.strip().splitlines()
        code = br.join(map(str.rstrip, lines)) + br
        return pattern.sub(2*br, code)

    @classmethod
    def submodule(cls, module: str, *objs: object) -> str:
        content = '\n\n'.join(cls.source(obj) for obj in objs)
        return f'class {module}(types.ModuleType):\n{cls._indent(content)}'

    @classmethod
    def _indent(cls, content: str, level: int = 1) -> str:
        return textwrap.indent(content, 4*level*' ')


p.Path('foam.py').write_text(show.code(f'''
import functools
import io
import json
import pathlib
import shlex
import shutil
import subprocess
import types
import typing
import warnings

if typing.TYPE_CHECKING:
    import numpy as np
    import vtkmodules as vtk

f = functools
p = pathlib
s = subprocess
t = typing
w = warnings

{Dict = !r}
{List = !r}
{Path = !r}

{show.source(Data)}

{show.source(progress.Default)}
{show.source(progress.AppBase)}
{show.source(progress.AppByTimeI)}
{show.source(progress.AppByTimeII)}
{show.source(progress.AppByIterationI)}
{show.source(progress.AppByIterationII)}
{show.source(progress.AppByProcessor)}

Apps = {show.apps(progress.Apps)}

{show.source(Command)}

{show.source(Parse)}

{show.submodule('postprocessing', VTK)}

{show.source(Foam)}
'''))
