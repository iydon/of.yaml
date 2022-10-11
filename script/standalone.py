import inspect
import pathlib as p
import re
import textwrap
import typing as t

from foam import app, base, compat, parse, util


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
import urllib.parse
import urllib.request
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
List = {base.type.List}
Path = {base.type.Path}

_NOT_FOUND = object()

class compat(types.ModuleType):
{show._indent(show.submodule('functools', compat.functools.cached_property, compat.functools.singledispatchmethod))}

f.cached_property = compat.functools.cached_property
f.singledispatchmethod = compat.functools.singledispatchmethod


{show.source(base.lib.lib)}
{show.source(base.type.Array)}
{show.source(base.type.Keys)}

{show.source(util.decorator.Match)}
{show.source(util.object.Data)}
{show.source(util.object.Version)}

{show.source(app.command.adapter.Default)}
{show.source(app.command.adapter.AppBase)}
{show.source(app.command.adapter.AppByTimeI)}
{show.source(app.command.adapter.AppByTimeII)}
{show.source(app.command.adapter.AppByIterationI)}
{show.source(app.command.adapter.AppByIterationII)}
{show.source(app.command.adapter.AppByProcessor)}

Apps = {{}} if lib['tqdm'] is None else {show.apps(app.command.adapter.Apps)}

{show.source(parse.static.Static)}
{show.source(parse.url.Url)}
{show.source(parse.yaml.YAML)}
{show.source(parse.Parser)}

{show.submodule('app', app.command.core.Command, app.information.core.Information, app.postprocess.core.PostProcess, app.postprocess.core.VTK)}

Command = app.Command
Information = app.Information
PostProcess = app.PostProcess
VTK = app.VTK

{show.source(base.core.Foam)}

__doc__ = Foam.__doc__
__license__ = """{util.function.license(full_text=False)}"""
__version__ = Foam.__version__
'''))
