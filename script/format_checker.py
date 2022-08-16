import pathlib as p
import re
import typing as t


class FormatChecker:
    funcs = []

    def __init__(
        self,
        root: t.Union[str, p.Path] = '.',
        prefixes: t.Set[str] = set(),
        suffixes: t.Set[str] = set(),
    ) -> None:
        self._root = p.Path(root)
        self._prefixes = prefixes
        self._suffixes = suffixes

    @classmethod
    def decorate(cls, func: t.Callable[[p.Path, str], t.Optional[str]]) -> None:
        cls.funcs.append(func)

    async def check(self) -> t.Iterator[t.Tuple[p.Path, str]]:
        for path, text in self._paths_and_texts():
            for func in self.funcs:
                message = await func(path, text)
                if message is not None:
                    yield path, message

    async def check_with(self, func: t.Callable) -> None:
        async for path, message in self.check():
            func(path, message)

    def _paths_and_texts(self) -> t.Iterator[t.Tuple[p.Path, str]]:
        for path in self._root.rglob('*'):
            if path.is_file():
                if path.parts[0] in self._prefixes or path.suffix in self._suffixes:
                    continue
                try:
                    text = path.read_text()
                except Exception as e:
                    print(e, path)
                else:
                    yield path, text


@FormatChecker.decorate
async def contain_space(path: p.Path, text: str) -> t.Optional[str]:
    if ' ' in str(path):
        return '[path: contain_space]'

@FormatChecker.decorate
async def trailing_whitespace(path: p.Path, text: str) -> t.Optional[str]:
    pattern = re.compile(r'[ \t]+\n')
    if pattern.search(text):
        return '[text: trailing_whitespace]'

@FormatChecker.decorate
async def tab(path: p.Path, text: str) -> t.Optional[str]:
    if '\t' in text:
        return '[text: tab]'

@FormatChecker.decorate
async def end_with_newline(path: p.Path, text: str) -> t.Optional[str]:
    if not text.endswith('\n'):
        return '[text: end_with_newline]'


if __name__ == '__main__':
    import asyncio

    fc = FormatChecker(
        root='.',
        prefixes={'.git', '.vscode'},
        suffixes={'.7z', '.dat', '.gz', '.mp4', '.pdf', '.png', '.whl'},
    )
    asyncio.run(fc.check_with(func=print))
