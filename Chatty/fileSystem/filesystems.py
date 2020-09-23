from typing import Union

from Chatty.fileSystem.fs import FileSystem

filesystems = {}


def add_filesystem(name: str, fs: FileSystem) -> None:
    filesystems[name] = fs


def access_fs(fs: str) -> Union[FileSystem, None]:
    if fs not in filesystems:
        raise Exception("[ERROR] ACCESS TO UNAVAILABLE FILESYSTEM")
    return filesystems[fs] if fs in filesystems else None


def try_access_fs(fs: str):
    return filesystems[fs] if fs in filesystems else None
