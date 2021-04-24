def format_timedelta(td):
    """Format timedelta to hours:minutes:seconds.

    Parameters:
        td (datetime.timedelta): Seconds in timedelta format

    Returns:
        str: Formatted string
    """
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)