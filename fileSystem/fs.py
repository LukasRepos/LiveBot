import os
import pathlib
from typing import AnyStr, TextIO

os.chdir(pathlib.Path(__file__).parent.parent.absolute())


"""def read(path: str) -> AnyStr:
    with open(path) as f:
        data = f.read()
    return data


def write(path: str, data: AnyStr) -> None:
    with open(path, "a") as f:
        f.write(data)


def get_stream(path: str) -> TextIO:
    return open(path)


def close_stream(filestream: TextIO) -> None:
    filestream.close()"""


class FileSystem:
    def __init__(self, root_folder: pathlib.PurePath) -> None:
        self.root = root_folder

    def read(self, path: str) -> AnyStr:
        os.chdir(pathlib.Path(self.root))
        with open(path) as f:
            data = f.read()
        return data

    def write(self, path: str, data: AnyStr) -> None:
        os.chdir(pathlib.Path(self.root))
        with open(path, "a") as f:
            f.write(data)

    def get_stream(self, path: str) -> TextIO:
        os.chdir(pathlib.Path(self.root))
        return open(path)

    def close_stream(self, filestream: TextIO) -> None:
        os.chdir(pathlib.Path(self.root))
        filestream.close()
