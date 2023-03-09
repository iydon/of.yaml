__all__ = ['Figure']


import pathlib as p
import typing as t

from ...function import deprecated_classmethod
from ....base.lib import matplotlib
from ....base.type import Path

if t.TYPE_CHECKING:
    import typing_extensions as te

    import matplotlib.axes as _axes
    import matplotlib.figure as _figure

    from . import mpl as _mpl, sns as _sns


class Figure:
    '''Matplotlib simple wrapper

    Example:
        >>> Figure.setRcParams(
        ...     ('axes.unicode_minus', False),
        ...     ('font.sans-serif', ['FandolHei']),
        ... )

        >>> Figure.new(figsize=(8, 6)) \\
        ...     .mpl.plot([1, 2, 3], [3, 2, 1], label='a') \\
        ...     .mpl.plot([1, 2, 3], [2, 1, 3], label='b') \\
        ...     .mpl.set(xlabel='x label', ylabel='y label', title='title') \\
        ...     .mpl.grid() \\
        ...     .mpl.legend() \\
        ...     .save('demo.png')
    '''

    _ax: '_axes.SubplotBase'
    _fig: '_figure.Figure'

    def __init__(self, **kwargs: t.Any) -> None:
        self._fig, self._ax = matplotlib.pyplot.subplots(1, 1, **kwargs)
        self._mpl = self._sns = None

    @classmethod
    def new(cls, **kwargs: t.Any) -> 'te.Self':
        return cls(**kwargs)

    @classmethod
    def setRcParams(cls, *items: t.Tuple[str, t.Any]) -> 'te.Self':
        # Type annotation of return value should actually be type
        for key, value in items:
            matplotlib.pyplot.rcParams[key] = value
        return cls

    @property
    def ax(self) -> '_axes.SubplotBase':
        return self._ax

    @property
    def fig(self) -> '_figure.Figure':
        return self._fig

    @property
    def mpl(self) -> '_mpl.AddOn':
        if self._mpl is None:
            from .mpl import AddOn

            self._mpl = AddOn.new(self)
        return self._mpl

    @property
    def sns(self) -> '_sns.AddOn':
        if self._sns is None:
            from .sns import AddOn

            self._sns = AddOn.new(self)

        return self._sns

    def save(self, path: Path, **kwargs: t.Any) -> 'te.Self':
        kwargs = {'bbox_inches': 'tight', 'transparent': False, **kwargs}
        self._fig.savefig(p.Path(path).as_posix(), **kwargs)
        return self

    set_rc_params = deprecated_classmethod(setRcParams)
