__all__ = ['Figure']


import pathlib as p
import typing as t

from ..function import deprecated_classmethod
from ...base.lib import matplotlib
from ...base.type import Path

if t.TYPE_CHECKING:
    import matplotlib.axes as _axes
    import matplotlib.figure as _figure

    from typing_extensions import Self


class Figure:
    '''Matplotlib simple wrapper

    Example:
        >>> Figure.setRcParams(
        ...     ('axes.unicode_minus', False),
        ...     ('font.sans-serif', ['FandolHei']),
        ... )
        >>> Figure.new(figsize=(8, 6)) \\
        ...     .plot([1, 2, 3], [3, 2, 1], label='a') \\
        ...     .plot([1, 2, 3], [2, 1, 3], label='b') \\
        ...     .set_ax(xlabel='x label', ylabel='y label', title='title') \\
        ...     .grid() \\
        ...     .legend() \\
        ...     .save('demo.png')
    '''

    DEFAULT = {
        'legend': {
            'bbox_to_anchor': (1.01, 1), 'loc': 'upper left',
            'borderaxespad': 0, 'ncol': 1,
        },
        'save': {'bbox_inches': 'tight', 'transparent': False},
    }

    _fig: '_figure.Figure'
    _ax: '_axes.SubplotBase'

    def __init__(self, **kwargs: t.Any) -> None:
        self._fig, self._ax = matplotlib.pyplot.subplots(1, 1, **kwargs)

    @classmethod
    def new(cls, **kwargs: t.Any) -> 'Self':
        return cls(**kwargs)

    @classmethod
    def setRcParams(cls, *items: t.Tuple[str, t.Any]) -> 'Self':
        # Type annotation of return value should actually be type
        plt = matplotlib.pyplot
        for key, value in items:
            plt.rcParams[key] = value
        return cls

    def grid(self, *args: t.Any, **kwargs: t.Any) -> 'Self':
        self._ax.grid(*args, **kwargs)
        return self

    def legend(self, *args: t.Any, **kwargs: t.Any) -> 'Self':
        kwargs = {**self.DEFAULT['legend'], **kwargs}
        self._ax.legend(*args, **kwargs)
        return self

    def plot(self, *args: t.Any, **kwargs: t.Any) -> 'Self':
        self._ax.plot(*args, **kwargs)
        return self

    def save(self, path: Path, **kwargs: t.Any) -> 'Self':
        kwargs = {**self.DEFAULT['save'], **kwargs}
        self._fig.savefig(p.Path(path).as_posix(), **kwargs)
        return self

    def set_ax(self, *args: t.Any, **kwargs: t.Any) -> 'Self':
        self._ax.set(*args, **kwargs)
        return self

    set_rc_params = deprecated_classmethod(setRcParams)
