def timedelta_to_string(timedelta):
    hours, minutes, details = str(timedelta).split(':')
    seconds = details[0:2]
    millis = details[3:6]
    micros = details[6:]

    if int(hours) > 0:
        return f'{hours}:{minutes}.{seconds}'
    if int(minutes) > 0:
        return f'{int(minutes)} minutes and {int(seconds)} seconds'
    if int(seconds) > 0:
        return f'{int(seconds)} seconds and {int(millis)} milliseconds'
    if int(millis) > 0:
        return f'{int(millis)} milliseconds'
    return f'{int(micros)} microseconds'
