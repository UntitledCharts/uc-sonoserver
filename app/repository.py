import asyncio
import hashlib
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from redis.asyncio import Redis

from app.sonolus_core import Srl

REPO_DATA_PREFIX = "repo:data:"
REPO_PATH_PREFIX = "repo:path:"


def sha1_hex(data: bytes) -> str:
    """Hash bytes with SHA-1.

    Args:
        data: Bytes to hash.

    Returns:
        str: Hex digest.
    """
    return hashlib.sha1(data).hexdigest()


def _read_zip_chain(root: Path, parts: list[str]) -> bytes:
    """Read a file through a chain of zips like ``a.zip|inner.zip|file.png``.

    Args:
        root: Folder the path is relative to.
        parts: File path followed by member names.

    Returns:
        bytes: The innermost file.
    """
    current = (root / parts[0]).read_bytes()
    for part in parts[1:]:
        with ZipFile(BytesIO(current)) as archive:
            try:
                current = archive.read(archive.getinfo(part))
            except KeyError:
                raise FileNotFoundError(f"{part} not found in zip chain") from None
    return current


def read_file_bytes(root: Path, file: str) -> bytes:
    """Read a file, following zip chains.

    Args:
        root: Folder the path is relative to.
        file: Relative path, optionally with ``|`` separated zip members.

    Returns:
        bytes: File contents.
    """
    if "|" in file:
        return _read_zip_chain(root, file.split("|"))
    return (root / file).read_bytes()


class Repository:
    """Static files hashed into Redis and served from ``/sonolus/repository/{hash}``.

    Attributes:
        _redis: Redis client.
        _root: Folder the stored file paths are relative to.
    """

    def __init__(self, redis: Redis, root: Path) -> None:
        """Create the repository.

        Args:
            redis: Redis client.
            root: Folder the stored file paths are relative to.
        """
        self._redis = redis
        self._root = root

    async def add_file(self, file: str, error_on_file_nonexistent: bool = True) -> str | None:
        """Store a file under its hash, dropping the blob of an older version.

        Args:
            file: Relative path like ``files/skins/x/data``, optionally with zip members.
            error_on_file_nonexistent: Raise when the file is missing instead of returning None.

        Returns:
            str | None: The SHA-1, or None for a missing optional file.
        """
        if not error_on_file_nonexistent and not (self._root / file.split("|")[0]).exists():
            return None
        data = await asyncio.to_thread(read_file_bytes, self._root, file)
        digest = sha1_hex(data)
        old_hash = await self._redis.get(REPO_PATH_PREFIX + file)
        if old_hash:
            old = old_hash.decode()
            if old != digest:
                await self._redis.delete(REPO_DATA_PREFIX + old)
        await self._redis.set(REPO_DATA_PREFIX + digest, data)
        await self._redis.set(REPO_PATH_PREFIX + file, digest)
        return digest

    async def add_bytes(self, data: bytes) -> str:
        """Store bytes under their hash unless already stored.

        Args:
            data: Bytes to store.

        Returns:
            str: The SHA-1.
        """
        digest = sha1_hex(data)
        if not await self._redis.exists(REPO_DATA_PREFIX + digest):
            await self._redis.set(REPO_DATA_PREFIX + digest, data)
        return digest

    async def get_file(self, digest: str) -> bytes | None:
        """Read a stored blob.

        Args:
            digest: SHA-1 of the blob.

        Returns:
            bytes | None: The blob, or None.
        """
        return await self._redis.get(REPO_DATA_PREFIX + digest)

    async def get_srl(self, digest: str | None) -> Srl | None:
        """Build the resource locator of a stored blob.

        Args:
            digest: SHA-1 of the blob.

        Returns:
            Srl | None: The locator, or None when the blob isn't stored.
        """
        if digest and await self._redis.exists(REPO_DATA_PREFIX + digest):
            return Srl(hash=digest, url=f"/sonolus/repository/{digest}")
        return None

    async def file_srl(self, file: str, error_on_file_nonexistent: bool = True) -> Srl | None:
        """Store a file and build its resource locator.

        Args:
            file: Relative path, optionally with zip members.
            error_on_file_nonexistent: Raise when the file is missing instead of returning None.

        Returns:
            Srl | None: The locator, or None for a missing optional file.
        """
        return await self.get_srl(await self.add_file(file, error_on_file_nonexistent))
