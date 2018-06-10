import pytest
try:
    import mock
except ImportError:
    from unittest import mock
from datetime import datetime, timedelta
from dateutil import tz
import tempfile
import time
import os
from dateutil.parser import parse

from watchdog import actions
from watchdog.misc import Message


class TestAction():
    def test___call__(monkeypatch):
        with pytest.raises(NotImplementedError):
            action = actions.Action()
            action(None, None, None)


class TestMessageAction():
    def test_inheritance(monkeypatch):
        action = actions.MessageAction()
        assert isinstance(action, actions.Action)

    def test__get_message(monkeypatch):
        action = actions.MessageAction(tzinfo='Asia/Tokyo')
        tick_time = parse('2017/10/10T02:03:04Z')
        estimated_trigger_time = parse('2017/05/10T03:04:05Z')
        trigger_time = parse('2017/10/05T11:11:11Z')
        message = Message(trigger_time, 10, 1, 2)

        expected_message = "Next trigger didn't come " \
                           "before the estimated time 2017-05-10T12:04:05+09:00 "\
                           "since 2017-10-05T20:11:11+09:00 at (epoch: 1, iteration: 2)."
        assert action._get_message(tick_time, estimated_trigger_time, message) == expected_message


class TestAbort():
    def test_inheritance(monkeypatch):
        action = actions.Abort()
        assert isinstance(action, actions.Action)

    @mock.patch('os.kill')
    def test___call__(monkeypatch, kill_mock):
        kill_mock.return_value = None
        pid = os.getpid()
        mysignal = 'hoge'
        action = actions.Abort(pid, signal=mysignal)
        now = datetime.now(tz.tzutc())
        message = Message(now, 10, 1, 2)

        action(now, now, message)
        kill_mock.assert_called_once_with(pid, mysignal)


class TestWarningMessageAction():
    def test_inheritance(monkeypatch):
        action = actions.WarningMessage()
        assert isinstance(action, actions.MessageAction)

    def test___call__(monkeypatch):
        action = actions.WarningMessage()
        now = datetime.now(tz.tzutc())
        message = Message(now, 10, 1, 2)

        action(now, now, message)


class TestSlackWebhookNotification():
    def test_inheritance(monkeypatch):
        action = actions.SlackWebhookNotification('url', 'channel')
        assert isinstance(action, actions.MessageAction)

    def test___call__(monkeypatch):
        url = 'url'
        channel = 'channel'
        action = actions.SlackWebhookNotification(url, channel, tzinfo='Asia/Tokyo')
        tick_time = parse('2017/10/10T02:03:04Z')
        estimated_trigger_time = parse('2017/05/10T03:04:05Z')
        trigger_time = parse('2017/10/05T11:11:11Z')
        message = Message(trigger_time, 10, 1, 2)

        with mock.patch.object(action._slack, 'notify') as slack_mock:
            slack_mock.return_value = None
            action(tick_time, estimated_trigger_time, message)
            expected_message = "Next trigger didn't come " \
                               "before the estimated time 2017-05-10T12:04:05+09:00 "\
                               "since 2017-10-05T20:11:11+09:00 at (epoch: 1, iteration: 2)."
            slack_mock.assert_called_once_with(channel=channel, text=expected_message)


class TestSlackTokenNotification():
    def test_inheritance(monkeypatch):
        action = actions.SlackNotification('token', 'channel')
        assert isinstance(action, actions.MessageAction)

    def test___call__(monkeypatch):
        token = 'token'
        channel = 'channel'
        action = actions.SlackNotification(token, channel, tzinfo='Asia/Tokyo')
        tick_time = parse('2017/10/10T02:03:04Z')
        estimated_trigger_time = parse('2017/05/10T03:04:05Z')
        trigger_time = parse('2017/10/05T11:11:11Z')
        message = Message(trigger_time, 10, 1, 2)

        with mock.patch.object(action._slack, 'api_call') as slack_mock:
            slack_mock.return_value = None
            action(tick_time, estimated_trigger_time, message)
            expected_message = "Next trigger didn't come " \
                               "before the estimated time 2017-05-10T12:04:05+09:00 "\
                               "since 2017-10-05T20:11:11+09:00 at (epoch: 1, iteration: 2)."
            slack_mock.assert_called_once_with('chat.postMessage', channel=channel, text=expected_message)

