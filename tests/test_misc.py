import pytest
try:
    import mock
except ImportError:
    from unittest import mock
from datetime import datetime, timedelta
from dateutil import tz

from watchdog import misc


class TestItem():
    def test___call__(monkeypatch):
        now = datetime.now(tz.tzutc())
        estimated = now + timedelta(seconds=2)
        action_mock = mock.Mock()
        estimator_mock = lambda *args: estimated
        watch_item = misc.WatchItem(action_mock, estimator_mock)
        message = 'hoge'

        action_mock.reset_mock()
        watch_item(now, message)
        action_mock.assert_not_called()

        action_mock.reset_mock()
        watch_item(now + timedelta(seconds=1), None)
        action_mock.assert_not_called()

        action_mock.reset_mock()
        watch_item(now + timedelta(seconds=2), None)
        action_mock.assert_not_called()

        action_mock.reset_mock()
        watch_item(now + timedelta(seconds=3), None)
        action_mock.assert_called_once_with(now + timedelta(seconds=3), estimated, message)

        action_mock.reset_mock()
        watch_item(now + timedelta(seconds=4), None)
        action_mock.assert_not_called()
