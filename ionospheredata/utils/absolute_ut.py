from datetime import date, timedelta


def absolute_ut(year, day_of_year, ms_of_day):
    """Computes absolute timestamp for a measurement
    :param year - number of year;
    :param day_of_year - number of day in the year. Sattellite data usually use this parameter instead of month/day;
    :param ms_of_day - relative number of milliseconds from the start of the day;
    :return seconds from the start of the epoche.
    """
    return int((date(year=int(year), month=1, day=1) + timedelta(days=int(day_of_year))).strftime('%s')) + ms_of_day / 1000.
