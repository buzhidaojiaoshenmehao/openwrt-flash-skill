import gzip
import hashlib
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/openwrt-flash/scripts/verify_firmware.py'
spec = importlib.util.spec_from_file_location('verify_firmware', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class VerifyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def sample(self, data, name='sample.img'):
        path = self.root / name
        path.write_bytes(data)
        return path, hashlib.sha256(data).hexdigest()

    def test_regular(self):
        path, digest = self.sample(b'firmware')
        result = module.verify(path, digest.upper())
        self.assertEqual(result['payload_bytes'], 8)
        self.assertFalse(result['gzip'])

    def test_gzip(self):
        path, digest = self.sample(gzip.compress(b'firmware'), 'sample.img.gz')
        result = module.verify(path, digest)
        self.assertEqual(result['payload_sha256'], hashlib.sha256(b'firmware').hexdigest())

    def test_multiple_members(self):
        path, digest = self.sample(gzip.compress(b'first') + gzip.compress(b'second'))
        self.assertEqual(module.verify(path, digest)['payload_bytes'], 11)

    def test_mismatch(self):
        path, _ = self.sample(b'firmware')
        with self.assertRaisesRegex(ValueError, 'mismatch'):
            module.verify(path, '0' * 64)

    def test_bad_digest(self):
        path, _ = self.sample(b'firmware')
        with self.assertRaises(ValueError):
            module.verify(path, 'not-a-digest')

    def test_empty(self):
        for data in (b'', gzip.compress(b'')):
            path, digest = self.sample(data)
            with self.assertRaisesRegex(ValueError, 'Empty'):
                module.verify(path, digest)

    def test_corrupt_gzip(self):
        data = bytearray(gzip.compress(b'firmware'))
        data[-8] ^= 255
        path, digest = self.sample(bytes(data))
        with self.assertRaises(OSError):
            module.verify(path, digest)

    def test_truncated_gzip(self):
        path, digest = self.sample(gzip.compress(b'firmware')[:-4])
        with self.assertRaises(EOFError):
            module.verify(path, digest)

    def test_suffix_mismatch(self):
        path, digest = self.sample(b'plain', 'sample.gz')
        with self.assertRaisesRegex(ValueError, 'gzip'):
            module.verify(path, digest)

    def test_limits(self):
        for data in (b'a' * 1024, gzip.compress(b'a' * 1024)):
            path, digest = self.sample(data)
            with self.assertRaisesRegex(ValueError, 'limit'):
                module.verify(path, digest, max_bytes=100)
        with self.assertRaises(ValueError):
            module.verify(path, digest, max_bytes=0)

    def test_directory(self):
        with self.assertRaises(ValueError):
            module.verify(self.root, '0' * 64)

    @unittest.skipUnless(os.name == 'posix', 'POSIX special files')
    def test_special_files(self):
        path, digest = self.sample(b'firmware')
        link = self.root / 'link'
        link.symlink_to(path)
        fifo = self.root / 'fifo'
        os.mkfifo(fifo)
        for target in (link, fifo, Path('/dev/null')):
            with self.assertRaises(ValueError):
                module.verify(target, digest)


if __name__ == '__main__':
    unittest.main()
