__all__ = ['solvers', 'utilities']


import os
import pathlib as p


if __name__ == '__main__':
    root = p.Path(os.environ['WM_PROJECT_DIR'])

    solvers = {
        path.parent.name: path.parent.relative_to(root).as_posix()
        for path in (root/'applications'/'solvers').rglob('*')
        if path.name == 'Make'
    }
    utilities = {
        path.parent.name: path.parent.relative_to(root).as_posix()
        for path in (root/'applications'/'utilities').rglob('*')
        if path.name == 'Make'
    }
