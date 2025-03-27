from datetime import datetime


def get_human_time(time: datetime):
    intervals = [29030400, 2419200, 604800, 86400, 3600, 60, 1]
    attrs = ['years', 'months', 'week', 'days', 'hours', 'minutes', 'seconds']
    times = []
    td = (datetime.now() - time).seconds
    for idx, attr in enumerate(attrs):
        if td > intervals[idx]:
            amount_of_times = td // intervals[idx]
            if amount_of_times > 1:
                attr_to_human = attr
            else:
                attr_to_human = attr[:-1]
            times.append(f'{amount_of_times} {attr_to_human}')
            td %= intervals[idx]
    if not times:
        times = ['0 seconds']
    return ', '.join(times)
