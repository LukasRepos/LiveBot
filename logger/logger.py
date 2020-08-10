import termcolor


def error(msg):
    termcolor.cprint(f"[ERROR] {msg}", "red")


def warning(msg):
    termcolor.cprint(f"[ERROR] {msg}", "yellow")


def log(msg):
    termcolor.cprint(f"{msg}", "grey")
