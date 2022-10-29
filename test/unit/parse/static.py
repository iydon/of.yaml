__all__ = ['Test']


import io
import json
import pathlib as p
import shutil
import time
import typing as t
import unittest

import py7zr

from foam import Foam
from foam.parse.static import Static


class Test(unittest.TestCase):
    '''Test for Static'''

    @classmethod
    def setUpClass(cls) -> None:
        cls._root = p.Path(__file__).parent
        cls._case = cls._root / 'case'
        cls._foam = Foam.from_demo('cavity', verbose=False)
        cls._foam.save(cls._case)
        cls._static = Static.from_foam(cls._foam)
        cls._content = p.Path(__file__).read_bytes()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls._case)

    def test_embed_text(self) -> None:
        path_dst = self._random_path(suffix='test')
        data = self._data(name=path_dst.name, types=['embed', 'text'], data='hello world!')
        self._process(data)
        self.assertTrue(path_dst.exists())
        self.assertEqual(path_dst.read_text(), data['data'])

    def test_embed_binary(self) -> None:
        path_dst = self._random_path(suffix='test')
        data = self._data(name=path_dst.name, types=['embed', 'binary'], data=b'hello world!')
        self._process(data)
        self.assertTrue(path_dst.exists())
        self.assertEqual(path_dst.read_bytes(), data['data'])

    def test_embed_7z(self) -> None:
        path_dst = self._random_path(suffix='py')
        data = self._data(name=path_dst.name, types=['embed', '7z'], data=self._7z(path_dst.name, self._content))
        self._process(data)
        self.assertTrue(path_dst.exists())
        self.assertEqual(path_dst.read_bytes(), self._content)

    def test_path_raw(self) -> None:
        path_dst = self._random_path(suffix='py')
        data = self._data(name=path_dst.name, types=['path', 'raw'], data=__file__)
        self._process(data)
        self.assertTrue(path_dst.exists())
        self.assertEqual(path_dst.read_bytes(), self._content)

    def test_path_7z(self) -> None:
        path_src = p.Path(__file__)
        path_dst = self._case / path_src.name
        path_7z = self._root / self._random_path(suffix='7z').name
        path_7z.write_bytes(self._7z(path_src.name, self._content))
        data = self._data(name=path_src.name, types=['path', '7z'], data=path_7z.as_posix())
        self._process(data)
        self.assertTrue(path_dst.exists())
        self.assertEqual(path_dst.read_bytes(), self._content)
        path_7z.unlink()

    def test_path_foam_json(self) -> None:
        path_src = self._root / self._random_path(suffix='json').name
        path_src.write_text(json.dumps({
            'FoamFile': {
                'version': 2.0,
                'format': 'ascii',
                'class': 'volVectorField',
                'object': 'U',
            },
            'dimensions': '[0 1 -1 0 0 0 0]',
            'internalField': 'uniform (0 0 0)',
            'boundaryField': {
                'movingWall': {
                    'type': 'fixedValue',
                    'value': 'uniform (1 0 0)',
                },
                'fixedWalls': {'type': 'noSlip'},
                'frontAndBack': {'type': 'empty'},
            },
        }))
        path_dst = self._random_path(suffix='foam')
        data = self._data(name=path_dst.name, types=['path', 'foam', 'json'], data=path_src.as_posix())
        self._process(data)
        self.assertTrue(path_dst.exists())
        self.assertListEqual(
            path_dst.read_text().splitlines(), [
                'FoamFile {version 2.0; format ascii; class volVectorField; object U;}',
                'dimensions [0 1 -1 0 0 0 0];',
                'internalField uniform (0 0 0);',
                'boundaryField {movingWall {type fixedValue; value uniform (1 0 0);} fixedWalls {type noSlip;} frontAndBack {type empty;}}',
            ],
        )
        path_src.unlink()

    def _data(
        self,
        name: str, types: t.List[str], data: t.Union[bytes, str],
        permission: t.Optional[int] = None,
    ) -> t.Dict[str, t.Any]:
        return {'name': name, 'type': types, 'permission': permission, 'data': data}

    def _process(self, data: t.Dict[str, t.Any]) -> None:
        self._static[tuple(data['type'])](data)

    def _random_path(self, suffix: str) -> p.Path:
        return self._case / f'{time.time_ns()}.{suffix}'

    def _7z(self, filename: str, content: bytes) -> bytes:
        with io.BytesIO() as f:
            with py7zr.SevenZipFile(f, 'w') as z:
                z.writestr(content, arcname=filename)
            return f.getvalue()
