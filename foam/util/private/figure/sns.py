__all__ = ['AddOn']


import typing as t

if t.TYPE_CHECKING:
    import typing_extensions as te

    from . import Figure


Wrapper = t.Callable[..., 'Figure']


class AddOn:
    '''seaborn

    TODO:
        - everything
    '''

    def __init__(self, figure: 'Figure') -> None:
        self._figure = figure
        self._ret = None

    @classmethod
    def new(cls, *args: t.Any, **kwargs: t.Any) -> 'te.Self':
        return cls(*args, **kwargs)

    @property
    def ret(self) -> t.Any:
        return self._ret

    def _wrapper(self, name: str, /, *args: t.Any, **kwargs: t.Any) -> 'Figure':
        self._ret = getattr(self._figure._ax, name)(*args, **kwargs)
        return self._figure
