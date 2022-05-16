import inspect
import pathlib as p
import re
import textwrap
import typing as t

from foam.app import command, information, postprocess
from foam.base import Foam, Parser, Array, Data, Dict, List, Path, Version, lib


class show:
    @classmethod
    def source(cls, obj: object) -> str:
        return inspect.getsource(obj)

    @classmethod
    def apps(cls, obj: t.Dict[str, t.Type]) -> str:
        content = ',\n'.join(
            f'{key!r}: {value.__name__}'
            for key, value in obj.items()
        )
        return f'{{\n{cls._indent(content)}\n}}'

    @classmethod
    def code(cls, obj: str) -> str:
        '''
        - Steps:
            1. convert type "Foam" to "'Foam'"
            2. remove relative imports
            3. remove trailing whitespace
            4. remove redundant line breaks
        '''
        br = '\n'
        pattern_im = re.compile(r'from \.[\w\.]* import \w+')
        pattern_br = re.compile(fr'{br}{{3,}}')
        step_1 = obj.replace(': Foam', ': \'Foam\'').replace(': t.Optional[Foam]', ': t.Optional[\'Foam\']')
        step_2 = pattern_im.sub('', step_1)
        step_3 = br.join(map(str.rstrip, step_2.strip().splitlines())) + br
        step_4 = pattern_br.sub(2*br, step_3)
        return step_4

    @classmethod
    def submodule(cls, module: str, *objs: object) -> str:
        content = '\n\n'.join(cls.source(obj) for obj in objs)
        return f'class {module}(types.ModuleType):\n{cls._indent(content)}'

    @classmethod
    def _indent(cls, content: str, level: int = 1) -> str:
        return textwrap.indent(content, 4*level*' ')


p.Path('foam.py').write_text(show.code(f'''
import collections
import functools
import gc
import io
import json
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import types
import typing
import warnings

if typing.TYPE_CHECKING:
    import numpy as np
    import vtkmodules as vtk

c = collections
f = functools
p = pathlib
s = subprocess
t = typing
w = warnings

{show.source(lib.__class__)}

lib = Lib.new()

{Dict = !r}
{List = !r}
{Path = !r}

{show.source(Array)}

{show.source(Data)}

{show.source(Version)}

{show.source(command.adapter.Default)}
{show.source(command.adapter.AppBase)}
{show.source(command.adapter.AppByTimeI)}
{show.source(command.adapter.AppByTimeII)}
{show.source(command.adapter.AppByIterationI)}
{show.source(command.adapter.AppByIterationII)}
{show.source(command.adapter.AppByProcessor)}

Apps = {{}} if lib['tqdm'] is None else {show.apps(command.adapter.Apps)}

{show.source(command.Command)}

{show.source(Parser)}

{show.submodule('app', command.Command, information.Information, postprocess.PostProcess, postprocess.VTK)}

Command = app.Command
Information = app.Information
PostProcess = app.PostProcess
VTK = app.VTK

{show.source(Foam)}
'''))
