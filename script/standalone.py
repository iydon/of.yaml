import inspect
import pathlib as p
import re
import textwrap
import typing as t

from foam.app import command, information, postprocess
from foam.base import Foam, Parser, Data, Dict, List, Path


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
            1. convert ": Foam" to ": 'Foam'"
            2. remove relative imports
            3. remove trailing whitespace
            4. remove redundant line breaks
        '''
        br = '\n'
        pattern_im = re.compile(r'from \.[\w\.]* import \w+')
        pattern_br = re.compile(fr'{br}{{3,}}')
        code = pattern_im.sub('', obj.replace(': Foam', ': \'Foam\''))
        code = br.join(map(str.rstrip, code.strip().splitlines())) + br
        return pattern_br.sub(2*br, code)

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
import io
import json
import os
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

c = collections
f = functools
p = pathlib
s = subprocess
t = typing
w = warnings

{Dict = !r}
{List = !r}
{Path = !r}

{show.source(Data)}

{show.source(command.adapter.Default)}
{show.source(command.adapter.AppBase)}
{show.source(command.adapter.AppByTimeI)}
{show.source(command.adapter.AppByTimeII)}
{show.source(command.adapter.AppByIterationI)}
{show.source(command.adapter.AppByIterationII)}
{show.source(command.adapter.AppByProcessor)}

Apps = {show.apps(command.adapter.Apps)}

{show.source(command.Command)}

{show.source(Parser)}

{show.submodule('app', command.Command, information.Information, postprocess.PostProcess)}

Command = app.Command
Information = app.Information
PostProcess = app.PostProcess

{show.source(Foam)}
'''))
