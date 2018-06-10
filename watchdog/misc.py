from datetime import datetime

from dateutil import tz

from six import string_types


class SimpleFormatter(object):
    def __init__(self, tzinfo=tz.tzlocal()):
        if isinstance(tzinfo, string_types):
            tzinfo = tz.gettz(tzinfo)
        self._tzinfo = tzinfo

    def __call__(self, key, value):
        if isinstance(value, datetime):
            value = value.replace(microsecond=0)
            if self._tzinfo is not None:
                value = value.astimezone(self._tzinfo)
            value = value.isoformat()
        return value


class Message(object):
    def __init__(self, trigger_time, elapsed_time, epoch_detail, iteration):
        assert trigger_time is not None
        assert elapsed_time is not None
        assert epoch_detail is not None
        assert iteration is not None

        self.trigger_time = trigger_time
        self.elapsed_time = elapsed_time
        self.epoch_detail = epoch_detail
        self.iteration = iteration


class WatchItem(object):
    def __init__(self, action, estimator):
        self._action = action
        self._estimator = estimator
        self._last_message = None
        self._estimated_trigger_time = None

    def __call__(self, tick_time, message):
        if message is not None:
            self._last_message = message
            self._estimated_trigger_time = self._estimator(message)
        else:
            if self._estimated_trigger_time is None or self._last_message is None:
                return
            if self._estimated_trigger_time < tick_time:
                self._action(tick_time, self._estimated_trigger_time, self._last_message)
                self._last_message = None
                self._estimated_trigger_time = None
