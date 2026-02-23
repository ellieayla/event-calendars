from datetime import timedelta


def to_string(delta: timedelta) -> str:
    """https://github.com/wimglenn/readabledelta/blob/master/readabledelta.py"""
    negative = delta < timedelta(0)
    delta = abs(delta)

    keys = 'weeks', 'days', 'hours', 'minutes', 'seconds', 'milliseconds', 'microseconds'
    # datetime.timedelta are normalized internally in Python to the units days, seconds, microseconds allowing a unique
    # representation.  This is not the only possible basis; the calculations below rebase onto more human friendly keys
    data = {}
    # rebase days onto weeks, days
    data['weeks'], data['days'] = divmod(delta.days, 7)
    # rebase seconds onto hours, minutes, seconds
    data['hours'], data['seconds'] = divmod(delta.seconds, 60*60)
    data['minutes'], data['seconds'] = divmod(data['seconds'], 60)
    # rebase microseconds onto milliseconds, microseconds
    data['milliseconds'], data['microseconds'] = divmod(delta.microseconds, 1000)

    output = ['{} {}'.format(data[k], k[:-1] if data[k] == 1 else k) for k in keys if data[k] != 0]

    if not output:
        result = 'an instant'
    elif len(output) == 1:
        [result] = output
    else:
        left, right = output[:-1], output[-1:]
        result = ', '.join(left) + ' and ' + right[0]

    if negative:
        result = '-' + result

    return result
