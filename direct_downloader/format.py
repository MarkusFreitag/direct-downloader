"""Submodule of direct_downloader, provides formatting helper methods."""


def sizeof_fmt(num):
    """Make an amount of bytes humanreadable with the correct unit.

    Args:
        num (int): amount of bytes
    Returns
        str: formated amount of bytes with unit
    """
    for unit in ['', 'Ki', 'Mi']:
        if abs(num) < 1024.0:
            return '{:3.2f}{}B'.format(num, unit)
        num /= 1024.0
    return '{:3.2f}GiB'.format(num)
