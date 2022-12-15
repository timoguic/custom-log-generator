from datetime import datetime as dt
from datetime import timedelta

import dateparser


class TimeProvider:
    def __init__(self, config):
        start = config.get("start")
        if not start:
            start = dt.now()
        else:
            start = dateparser.parse(
                config["start"],
                settings={"DATE_ORDER": "DMY", "PREFER_LOCALE_DATE_ORDER": False},
            )

        self.current_time = start
        self.interval = config["interval"]

    @property
    def timestamp(self):
        cur_time = self.current_time
        self.current_time = self.current_time + timedelta(seconds=self.interval)
        return cur_time
