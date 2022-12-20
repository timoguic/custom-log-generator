from datetime import datetime as dt
from datetime import timedelta

import dateparser


class TimeProvider:
    """Manages and keeps track of time"""

    def __init__(self, interval, start=None, office_hours=None):
        if not start:
            start = dt.now()
        else:
            start = dateparser.parse(
                start,
                settings={"DATE_ORDER": "YMD", "PREFER_LOCALE_DATE_ORDER": False},
            )

        self.office_hours = None
        if office_hours:
            self.office_hours = {
                "start": office_hours["start"],
                "end": office_hours["end"],
            }

        self._current_time = start
        self.current_time = start
        self.interval = interval

    @property
    def current_time(self):
        return self._current_time

    @current_time.setter
    def current_time(self, value):
        if not self.office_hours:
            self._current_time = value
            return

        office_start = dt(
            self._current_time.year,
            self._current_time.month,
            self._current_time.day,
            self.office_hours["start"],
            0,
        )
        office_end = dt(
            self._current_time.year,
            self._current_time.month,
            self._current_time.day,
            self.office_hours["end"],
            0,
        )

        if office_start <= value <= office_end:
            self._current_time = value
            return

        if value < office_start:
            # Skip to first working hour, same day
            self._current_time = office_start
        elif value > office_end:
            # Skip to next working day, starting hour
            self._current_time = office_start + timedelta(days=1)

    @property
    def timestamp(self):
        cur_time = self.current_time
        self.current_time = self.current_time + timedelta(seconds=self.interval)
        return cur_time
