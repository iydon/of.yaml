import json
import os
import pathlib as p
import re


def strip(text: str) -> str:
    # step 1
    pattern = re.compile(r'(/\*)([\s\S]+?)(\*/)')
    text = pattern.sub('', text)
    # step 2
    pattern = re.compile(r'(\\)([^\n]*)(\n)')
    text = pattern.sub('', text)
    # step 3
    pattern = re.compile(r' {2,}')
    text = pattern.sub(' ', text)
    # step 4
    pattern = re.compile(r'\n{2,}')
    text = pattern.sub('\n', text)
    # step 5
    return text.strip()


root = p.Path(os.environ['WM_PROJECT_DIR'])
makes = {}
for path in root.rglob('*'):
    if path.is_dir() and path.name=='Make':
        makes[path.relative_to(root).as_posix()] = {
            file.name: strip(file.read_text()).splitlines()
            for file in path.iterdir()
        }
with open('wmake.json', 'w') as f:
    json.dump(makes, f, indent=4)
