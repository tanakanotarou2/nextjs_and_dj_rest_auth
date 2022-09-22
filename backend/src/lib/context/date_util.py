import datetime

from django.utils import timezone as dj_timezone

from lib.interfaces.context.date_util import DateUtil


class DjangoDateUtil(DateUtil):
    def now(self) -> datetime.datetime:
        return dj_timezone.now()

    def local_now(self) -> datetime.datetime:
        return dj_timezone.localtime()

    def make_aware(self, value, timezone=None, is_dst=None):
        return dj_timezone.make_aware(value, timezone, is_dst)
