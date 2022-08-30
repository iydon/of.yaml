import collections as c
import subprocess


def stdout(command: str) -> str:
    cp = subprocess.run(command, capture_output=True, shell=True)
    return cp.stdout.decode()

def is_valid(line: str) -> bool:
    return line.startswith('foam')


if __name__ == '__main__':
    mapper = {'error': '🛑', 'note': '⚠️'}
    hash = stdout('git rev-parse HEAD').strip()

    lines = c.defaultdict(list)
    for line in stdout('make mypy').splitlines():
        if is_valid(line):
            path, number, type, message = map(str.strip, line.split(':', maxsplit=3))
            tag = mapper.get(type, '❓')
            url = f'https://github.com/iydon/of.yaml/blob/{hash}/{path}#L{number}'
            line = f'- [ ] {tag} [{path}]({url}): `{message}`'
            lines[type].append(line)

    with open('mypy.md', 'w') as f:
        for value in lines.values():
            f.write('\n'.join(value))
        f.write('\n')
