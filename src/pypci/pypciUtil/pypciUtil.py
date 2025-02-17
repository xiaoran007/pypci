import platform


def getOS():
    """
    Get the os type in lower case.
    :return: str, os type, value in [windows, linux, macos, freebsd, unknown].
    """
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "macos"
    elif system == "FreeBSD":
        return "freebsd"
    else:
        return "unknown"
