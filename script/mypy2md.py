import collections as c
import re
import subprocess


def stdout(command: str) -> str:
    cp = subprocess.run(command, capture_output=True, shell=True)
    return cp.stdout.decode()

def is_valid(line: str) -> bool:
    return line.startswith('foam')


if __name__ == '__main__':
    mapper = {'error': '🛑', 'note': '⚠️'}
    hash = stdout('git rev-parse HEAD').strip()
    patterns = [
        re.compile(r'Name "t\.Self" is not defined'),
        re.compile(r'Skipping analyzing "[a-zA-Z0-9_\.]+": module is installed, but missing library stubs or py\.typed marker')
    ]
    is_remote = True

    prefix = f'https://github.com/iydon/of.yaml/blob/{hash}/' if is_remote else ''
    lines = c.defaultdict(list)
    for line in stdout('make mypy').splitlines():
        if is_valid(line):
            path, number, type, message = map(str.strip, line.split(':', maxsplit=3))
            if any(p.match(message) for p in patterns):
                continue
            tag = mapper.get(type, '❓')
            url = f'{prefix}{path}#L{number}'
            line = f'- [ ] {tag} [{path}]({url}): `{message}`'
            lines[type].append(line)

    with open('mypy.md', 'w') as f:
        for value in lines.values():
            f.write('\n'.join(value))
            f.write('\n')
