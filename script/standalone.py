import inspect
import pathlib as p
import re
import textwrap
import typing as t

from foam import app, base, compat


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
import _thread
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
import sys
import types
import typing
import urllib
import warnings

if typing.TYPE_CHECKING:
    import vtkmodules as vtk

    from typing_extensions import Self

c = collections
f = functools
p = pathlib
s = subprocess
t = typing
w = warnings

CachedLib = {repr(base.type.CachedLib).replace('module', 'types.ModuleType')}
Dict = {base.type.Dict}
Keys = {base.type.Keys}
List = {base.type.List}
Path = {base.type.Path}

_NOT_FOUND = object()

class compat(types.ModuleType):
{show._indent(show.submodule('functools', compat.functools.cached_property, compat.functools.singledispatchmethod))}

for obj, name in [
    (f, 'cached_property'),
    (f, 'singledispatchmethod'),
]:
    if not hasattr(obj, name):
        setattr(obj, name, getattr(getattr(compat, obj.__name__), name))


{show.source(base.lib.lib.__class__)}

lib = Lib.default()

{show.source(base.type.Array)}

{show.source(base.type.Data)}

{show.source(base.type.Version)}

{show.source(app.command.adapter.Default)}
{show.source(app.command.adapter.AppBase)}
{show.source(app.command.adapter.AppByTimeI)}
{show.source(app.command.adapter.AppByTimeII)}
{show.source(app.command.adapter.AppByIterationI)}
{show.source(app.command.adapter.AppByIterationII)}
{show.source(app.command.adapter.AppByProcessor)}

Apps = {{}} if lib['tqdm'] is None else {show.apps(app.command.adapter.Apps)}

{show.source(base.parse.register)}
{show.source(base.parse.Static)}
{show.source(base.parse.Url)}
{show.source(base.parse.YAML)}
{show.source(base.parse.Parser)}

{show.submodule('app', app.command.core.Command, app.information.core.Information, app.postprocess.core.PostProcess, app.postprocess.core.VTK)}

Command = app.Command
Information = app.Information
PostProcess = app.PostProcess
VTK = app.VTK

{show.source(base.core.Foam)}
'''))
