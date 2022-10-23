import inspect
import pathlib as p
import re
import textwrap
import typing as t

import foam

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
        return f'{{\n{cls.indent(content)}\n}}'

    @classmethod
    def code(cls, obj: str) -> str:
        '''
        - Steps:
            1. remove relative imports
            2. remove trailing whitespace
            3. remove redundant line breaks
        '''
        br = '\n'
        pattern_im = re.compile(r'from \.[\w.]* import \w+')
        pattern_br = re.compile(fr'{br}{{3,}}')
        # step_1 = obj.replace(': Foam', ': \'Foam\'').replace(': t.Optional[Foam]', ': t.Optional[\'Foam\']')
        step_1 = pattern_im.sub('', obj)
        step_2 = br.join(map(str.rstrip, step_1.strip().splitlines())) + br
        step_3 = pattern_br.sub(2*br, step_2)
        return step_3

    @classmethod
    def submodule(cls, module: str, *objs: object) -> str:
        content = '\n\n'.join(cls.source(obj) for obj in objs)
        return f'class {module}(types.ModuleType):\n{cls.indent(content)}'

    @classmethod
    def indent(cls, content: str, level: int = 1) -> str:
        return textwrap.indent(content, 4*level*' ')


p.Path('foam.py').write_text(show.code(f'''
__all__ = {foam.__all__}

import _thread
import collections
import contextlib
import email.message
import email.utils
import functools
import gc
import io
import json
import mimetypes
import os
import pathlib
import pickle
import re
import shlex
import shutil
import smtplib
import subprocess
import sys
import time
import types
import typing
import urllib.parse
import urllib.request
import warnings

if typing.TYPE_CHECKING:
    import lark as _lark
    import matplotlib as _matplotlib
    import matplotlib.axes as _axes
    import matplotlib.figure as _figure
    import matplotlib.pyplot as _pyplot
    import numpy as _numpy
    import py7zr as _py7zr
    import tqdm as _tqdm
    import vtkmodules as _vtkmodules
    import yaml as _yaml

    from email.message import EmailMessage

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
FoamItem = {base.type.FoamItem}
FoamData = {base.type.FoamData}
Location = {base.type.Location}
Path = {base.type.Path}

_NOT_FOUND = object()

class compat(types.ModuleType):
{show.indent(show.submodule('functools', compat.functools.cached_property, compat.functools.singledispatchmethod))}
{show.indent(show.submodule('shutil', compat.shutil.copytree))}

f.cached_property = compat.functools.cached_property
f.singledispatchmethod = compat.functools.singledispatchmethod
shutil.copytree = compat.shutil.copytree

# util.decorator.classproperty
{show.source(base.lib.classproperty)}
{show.source(base.lib.lark)}
{show.source(base.lib.matplotlib)}
{show.source(base.lib.numpy)}
{show.source(base.lib.py7zr)}
{show.source(base.lib.tqdm)}
{show.source(base.lib.vtkmodules)}
{show.source(base.lib.yaml)}
{show.source(base.type.Array)}
{show.source(base.type.Keys)}

{show.source(util.deprecation.lib)}
{show.source(util.decorator.Match)}
{show.source(util.object.data.Data)}
{show.source(util.object.email.Envelope)}
{show.source(util.object.email.SMTP)}
{show.source(util.object.figure.Figure)}
{show.source(util.object.timer.Timer)}
{show.source(util.object.version.Version)}

{show.source(app.command.adapter.Default)}
{show.source(app.command.adapter.AppBase)}
{show.source(app.command.adapter.AppByTimeI)}
{show.source(app.command.adapter.AppByTimeII)}
{show.source(app.command.adapter.AppByIterationI)}
{show.source(app.command.adapter.AppByIterationII)}
{show.source(app.command.adapter.AppByProcessor)}

Apps = {{}} if tqdm.is_not_available() else {show.apps(app.command.adapter.Apps)}

{show.source(parse.lark.Lark).replace('grammar()', '__grammar__')}
{show.source(parse.static.Static)}
{show.source(parse.url.Url)}
{show.source(parse.yaml.YAML)}
{show.source(parse.Parser)}

{show.source(app.command.core.Command)}
{show.source(app.information.core.Information)}
{show.source(app.postprocess.core.PostProcess)}
{show.source(app.postprocess.core.VTK)}

{show.source(base.core.Foam)}

__doc__ = Foam.__doc__
__grammar__ = r"""{util.function.grammar()}"""
__license__ = r"""{util.function.license(full_text=False)}"""
__version__ = Foam.__version__
'''))
