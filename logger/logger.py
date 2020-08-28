import termcolor

from fileSystem import fs


redirect = False


def error(msg: str, to_file=False) -> None:
    if to_file or redirect:
        fs.write("./logger/log.txt", f"[ERROR] {msg}\n")
    else:
        termcolor.cprint(f"[ERROR] {msg}", "red")


def warning(msg: str, to_file=False) -> None:
    if to_file or redirect:
        fs.write("./logger/log.txt", f"[WARNING] {msg}\n")
    else:
        termcolor.cprint(f"[WARNING] {msg}", "yellow")


def log(msg: str, to_file=False) -> None:
    if to_file or redirect:
        fs.write("./logger/log.txt", msg)
    else:
        termcolor.cprint(f"{msg}\n", "grey")
