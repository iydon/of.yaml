import inspect
import pathlib as p
import re
import textwrap
import typing as t

from foam import Foam
from foam.command import Command, progress
from foam.parse import Parse
from foam.type import Dict, List, Path, Data


class show:
    @staticmethod
    def source(obj: object) -> str:
        pattern = re.compile(r'from \.[\w\.]* import \w+')
        content = inspect.getsource(obj)
        return pattern.sub('', content)

    @staticmethod
    def apps(obj: t.Dict[str, t.Type]) -> str:
        content = ',\n'.join(
            f'{key!r}: {value.__name__}'
            for key, value in obj.items()
        )
        return '{\n' + textwrap.indent(content, '    ') + '\n}'

    @staticmethod
    def code(obj: str) -> str:
        br = '\n'
        lines = obj.strip().splitlines()
        code = br.join(map(str.rstrip, lines)) + br
        return code.replace(3*br, 2*br)


p.Path('foam.py').write_text(show.code(f'''
import functools
import io
import json
import pathlib
import shlex
import shutil
import subprocess
import typing
import warnings

f = functools
p = pathlib
s = subprocess
t = typing

{Dict = !r}
{List = !r}
{Path = !r}

{show.source(Data)}

{show.source(progress.Default)}
{show.source(progress.AppBase)}
{show.source(progress.AppByTime)}
{show.source(progress.AppByIterationI)}
{show.source(progress.AppByIterationII)}

Apps = {show.apps(progress.Apps)}

{show.source(Command)}

{show.source(Parse)}

{show.source(Foam)}
'''))
