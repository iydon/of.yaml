__all__ = ['Protocol']


try:
    from typing_extensions import Protocol
except ModuleNotFoundError:
    Protocol = object
