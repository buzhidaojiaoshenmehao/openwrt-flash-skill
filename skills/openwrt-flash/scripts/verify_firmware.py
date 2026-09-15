#!/usr/bin/env python3
"""Read-only checksum and gzip integrity checks, never a flashing tool."""

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import zlib

CHUNK = 1024 * 1024


def measure(stream, limit):
    digest = hashlib.sha256()
    size = 0
    while True:
        block = stream.read(min(CHUNK, limit - size + 1))
        if not block:
            break
        size += len(block)
        if size > limit:
            raise ValueError("File exceeds the configured byte limit")
        digest.update(block)
    if not size:
        raise ValueError("Empty firmware payload")
    return size, digest.hexdigest()


def verify(path, expected, max_bytes=16 * 1024**3):
    if not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
        raise ValueError("Expected SHA-256 must contain exactly 64 hexadecimal digits")
    if max_bytes <= 0:
        raise ValueError("Byte limit must be positive")
    path = Path(path)
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise ValueError("Only regular files are allowed; no symlinks or devices")
    # NONBLOCK prevents a raced replacement by a FIFO from blocking on open.
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    with os.fdopen(os.open(path, flags), "rb") as stream:
        opened = os.fstat(stream.fileno())
        if not stat.S_ISREG(opened.st_mode) or (before.st_dev, before.st_ino) != (
            opened.st_dev, opened.st_ino
        ):
            raise ValueError("File changed during opening")
        size, digest = measure(stream, max_bytes)
        if digest != expected.lower():
            raise ValueError("SHA-256 mismatch")
        stream.seek(0)
        compressed = stream.read(2) == b"\x1f\x8b"
        if path.suffix.lower() == ".gz" and not compressed:
            raise ValueError("A .gz file must contain gzip data")
        stream.seek(0)
        if compressed:
            with gzip.GzipFile(fileobj=stream) as payload:
                payload_size, payload_digest = measure(payload, max_bytes)
        else:
            payload_size, payload_digest = size, digest
        after = os.fstat(stream.fileno())
        if (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) != (
            after.st_size, after.st_mtime_ns, after.st_ctime_ns
        ):
            raise ValueError("File changed during verification")
    return {
        "sha256": digest,
        "file_bytes": size,
        "gzip": compressed,
        "payload_bytes": payload_size,
        "payload_sha256": payload_digest,
        "scope": "Checksum/integrity only; not signature, compatibility or disk authorization",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--sha256", required=True, help="Digest from a trusted manifest")
    parser.add_argument("--max-bytes", type=int, default=16 * 1024**3,
                        help="Maximum compressed and expanded bytes (default: 16 GiB)")
    args = parser.parse_args()
    try:
        result = verify(args.file, args.sha256, args.max_bytes)
    except (OSError, ValueError, EOFError, zlib.error) as error:
        print("Verification failed: " + str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
