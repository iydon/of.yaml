'''Draft conversion of OpenFOAM case to YAML format
'''
import os
import pathlib as p
import re
import subprocess
import textwrap
import typing as t

from foam import __version__


Path = t.Union[str, p.Path]


class Case:
    Self = __qualname__
    version = __version__
    keys = [('0',), ('constant',), ('system',)]

    def __init__(self, path: Path, threshold: int) -> None:
        self._threshold = threshold
        self._root = p.Path(os.environ['WM_PROJECT_DIR'])
        self._origin = p.Path(path)
        self._target = self._origin.relative_to(self._root).parent / f'{self._origin.name}.yaml'
        self._target.parent.mkdir(parents=True, exist_ok=True)
        self._foam, self._static, self._todos = self._categorize()
        self._todo()

    def __repr__(self) -> str:
        return f'<Case from "{self._origin}" to "{self._target}">'

    @classmethod
    def from_path(cls, path: Path, threshold: int = 1024) -> Self:
        return cls(path, threshold)

    def save(self) -> Self:
        parts = self._part_meta(), self._part_foam(), self._part_static(), self._part_other()
        text = '---\n' + '\n---\n'.join(map(self._post_process, parts)) + '\n'
        self._target.write_text(text)
        return self

    def readme(self) -> str:
        version = os.environ['WM_PROJECT_VERSION']
        target = self._target.as_posix()
        url = f'https://github.com/OpenFOAM/OpenFOAM-7/tree/master/{target.replace(".yaml", "")}'
        index = next(ith for ith, part in enumerate(self._target.parts) if part.endswith('Foam'))
        solver = '/'.join(self._target.parts[index-1:index+1])
        cp = subprocess.run(f'find $FOAM_APP -name {self._target.parts[index]}', capture_output=True, shell=True)
        path = p.Path(cp.stdout.decode().strip()).relative_to(self._root).as_posix()
        return f'| [{self._target.name}]({target}) | [{self._origin.name}]({url}) | {version} | [{solver}](https://github.com/OpenFOAM/OpenFOAM-{version}/tree/master/{path}) |'

    def _categorize(self) -> t.Tuple[t.Dict[t.Tuple[str, ...], str], ...]:
        foam, static, todos = {}, {}, {}
        for path in self._origin.rglob('*'):
            if path.is_file():
                *keys, value = path.relative_to(self._origin).parts
                keys = tuple(keys)
                if path.stat().st_size > self._threshold:
                    todos.setdefault(keys, []).append(value)
                elif keys in self.keys:
                    foam.setdefault(keys, []).append(value)
                else:
                    static.setdefault(keys, []).append(value)
        return map(
            lambda data: {k: sorted(v) for k, v in data.items()},
            [foam, static, todos],
        )

    def _todo(self) -> None:
        print('TODO:')
        for keys, values in self._todos.items():
            for value in values:
                path = self._origin / p.Path(*keys) / value
                print('-', path)

    def _part_meta(self) -> str:
        return f'''
            openfoam: [{os.environ['WM_PROJECT_VERSION']}]
            version: {__version__}
            order:
                - meta
                - foam
                - static
                - other
        '''

    def _part_foam(self) -> str:
        template = '''
            {value}:
                FoamFile:
                    class: TODO
                    object: TODO
                    <<: *FoamFile{data}
        '''.rstrip()[1:]
        texts = []
        for keys in self.keys:
            texts.append(f'        {keys[-1]}:')
            for value in self._foam.get(keys, []):
                path = self._origin / p.Path(*keys) / value
                data = '\n' + self._indent(self._pre_process(path.read_text()), 16)
                texts.append(template.format(value=value, data=data))
        return '\n'.join(texts) \
            .replace('0:\n', '"0":\n') \
            .replace(';\n', '\n') \
            .replace('\n\n', '\n')

    def _part_static(self) -> str:
        template = '''
        -
            name: {name}
            type: [embed, text]
            permission: 777
            data: {data}
        '''.rstrip()[1:]
        texts = []
        for keys, values in self._static.items():
            for value in values:
                path = self._origin / p.Path(*keys) / value
                name = path.relative_to(self._origin).as_posix()
                data = '|\n' + self._indent(self._pre_process(path.read_text()), 16)
                texts.append(template.format(name=name, data=data))
        return '\n'.join(texts)

    def _part_other(self) -> str:
        return '''
            pipeline:
                - TODO
        '''

    def _indent(self, text: str, size: int = 4) -> str:
        return textwrap.indent(text, prefix=size*' ')

    def _dedent(self, text: str) -> str:
        return textwrap.dedent(text)

    def _pre_process(self, text: str) -> str:
        pattern_comment = re.compile(r'/\*[\s\S]+?\*/')
        pattern_newline = re.compile(r'\n{3,}')
        step_0 = text.strip() + '\n'
        step_1 = pattern_comment.sub('', step_0)
        step_2 = '\n'.join(map(str.rstrip, step_1.splitlines()))
        step_3 = pattern_newline.sub('\n\n', step_2)
        return step_3.strip()

    def _post_process(self, text: str) -> str:
        return self._dedent(text).strip()


if __name__ == '__main__':
    path = input('(path) >>> ')
    case = Case.from_path(path=path, threshold=16*1024).save()
    print(case.readme())
