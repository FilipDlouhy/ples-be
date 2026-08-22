# Half-hour slots of the salon on the day of the ball, the keys of the Laravel MakerController
TIME_SLOTS = ["1400", "1430", "1500", "1530", "1600", "1630", "1700", "1730", "1800", "1830"]


def format_time(time_slot):
    """Turn 1430 into 14:30."""
    return f"{time_slot[:2]}:{time_slot[2:]}"
