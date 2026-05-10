from datetime import timedelta


def td_format(td_object: timedelta):
    seconds = int(td_object.total_seconds())
    if seconds < 0:
        return None

    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)

    if days > 0:
        return f"{days}d {hours:02}:{minutes:02}:{secs:02}"
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{secs:02}"
    if minutes > 0:
        return f"{minutes:02}:{secs:02}"
    return f"{secs}s"


# print(td_format(timedelta(seconds=1.2)))
