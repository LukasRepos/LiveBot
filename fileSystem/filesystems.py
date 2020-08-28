from typing import Union

from fileSystem.fs import FileSystem

filesystems = {}


def add_filesystem(name: str, fs: FileSystem) -> None:
    filesystems[name] = fs


def access_fs(fs: str) -> Union[FileSystem, None]:
    return filesystems[fs] if fs in filesystems else None
