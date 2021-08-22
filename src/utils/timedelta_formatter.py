"""Timedelta formatter.

This script allows to format a given timedelta to a specific look.

This file can also be imported as a module and contains the following functions:
    * format_timedelta - formats timedelta to hours:minutes:seconds
"""


def format_timedelta(td):
    """Format timedelta to hours:minutes:seconds.

    Args:
        td (datetime.timedelta): Seconds in timedelta format

    Returns:
        str: Formatted string
    """
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)
