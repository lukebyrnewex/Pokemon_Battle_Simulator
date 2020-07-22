def pandas_series_to_int_list(series):
    """Transform int series into a list of ints."""
    int_list = []
    for stats in series.iteritems():
        int_list.append(stats[1])
    return int_list
