import datetime
from abc import ABC, abstractmethod
from typing import Union


class DateUtil(ABC):
    @abstractmethod
    def now(self) -> datetime.datetime:
        raise NotImplementedError()

    def today(self) -> datetime.date:
        return self.now().date()

    @abstractmethod
    def local_now(self) -> datetime.datetime:
        raise NotImplementedError()

    def local_today(self) -> datetime.date:
        return self.local_now().date()

    def add_days(
        self, value: Union[datetime.datetime, datetime.date], days
    ) -> Union[datetime.datetime, datetime.date]:
        return value + datetime.timedelta(days=days)

    def add_time(
        self, value: Union[datetime.datetime, datetime.date], days=0, hours=0, minutes=0, seconds=0, microseconds=0
    ) -> Union[datetime.datetime, datetime.date]:
        return value + datetime.timedelta(
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            microseconds=microseconds,
        )

    def make_aware(self, value, timezone=None, is_dst=None):
        raise NotImplementedError()
