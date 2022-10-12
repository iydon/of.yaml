__all__ = ['argmin', 'is_tqdm_available', 'load_7z', 'load_text', 'progress_bar', 'square', 'vtk_generic_data_object_reader', 'vtk_to_numpy', 'yaml_dump_all', 'yaml_load', 'yaml_load_all']


import pathlib as p
import typing as t

if t.TYPE_CHECKING:
    import numpy as np
    import py7zr
    import tqdm
    import vtkmodules.all


root = p.Path(__file__).parents[1]


def argmin(*args: t.Any, **kwargs: t.Any) -> 'np.ndarray':
    try:
        import numpy as np
    except Exception as e:
        raise e.__class__('pip install ifoam[vtk]')

    return np.argmin(*args, **kwargs)


def is_tqdm_available() -> bool:
    try:
        import tqdm
    except:
        return False
    else:
        return True


def load_7z(*args: t.Any, **kwargs: t.Any) -> 'py7zr.SevenZipFile':
    try:
        import py7zr
    except Exception as e:
        raise e.__class__('pip install ifoam[7z]')

    return py7zr.SevenZipFile(*args, **kwargs)


def load_text(*args: t.Any, **kwargs: t.Any) -> 'np.ndarray':
    try:
        import numpy as np
    except Exception as e:
        raise e.__class__('pip install ifoam[vtk]')

    return np.loadtxt(*args, **kwargs)


def progress_bar(*args: t.Any, **kwargs: t.Any) -> 'tqdm.std.tqdm':
    try:
        import tqdm
    except Exception as e:
        raise e.__class__('pip install ifoam[tqdm]')

    return tqdm.tqdm(*args, **kwargs)


def square(*args: t.Any, **kwargs: t.Any) -> 'np.ndarray':
    try:
        import numpy as np
    except Exception as e:
        raise e.__class__('pip install ifoam[vtk]')

    return np.square(*args, **kwargs)


def vtk_generic_data_object_reader(*args: t.Any, **kwargs: t.Any) -> 'vtkmodules.vtkIOLegacy.vtkGenericDataObjectReader':
    try:
        import vtkmodules.all as vtk
    except Exception as e:
        raise e.__class__('pip install ifoam[vtk]')

    return vtk.vtkGenericDataObjectReader()


def vtk_to_numpy(*args: t.Any, **kwargs: t.Any) -> 'np.ndarray':
    try:
        from vtkmodules.util.numpy_support import vtk_to_numpy
    except Exception as e:
        raise e.__class__('pip install ifoam[vtk]')

    return vtk_to_numpy(*args, **kwargs)


def yaml_dump_all(*args: t.Any, **kwargs: t.Any) -> str:
    try:
        import yaml
        try:
            from yaml import CSafeLoader as SafeLoader
        except ImportError:
            from yaml import SafeLoader
    except Exception as e:
        raise e.__class__('pip install ifoam')

    kwargs['Loader'] = SafeLoader
    return yaml.dump_all(*args, **kwargs)


def yaml_load(*args: t.Any, **kwargs: t.Any) -> t.Any:
    try:
        import yaml
        try:
            from yaml import CSafeLoader as SafeLoader
        except ImportError:
            from yaml import SafeLoader
    except Exception as e:
        raise e.__class__('pip install ifoam')

    kwargs['Loader'] = SafeLoader
    return yaml.load(*args, **kwargs)


def yaml_load_all(*args: t.Any, **kwargs: t.Any) -> t.Iterator[t.Any]:
    try:
        import yaml
        try:
            from yaml import CSafeLoader as SafeLoader
        except ImportError:
            from yaml import SafeLoader
    except Exception as e:
        raise e.__class__('pip install ifoam')

    kwargs['Loader'] = SafeLoader
    return yaml.load_all(*args, **kwargs)
