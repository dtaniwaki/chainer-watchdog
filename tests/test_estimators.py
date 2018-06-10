import pytest
try:
    import mock
except ImportError:
    from unittest import mock
from datetime import datetime, timedelta
import tempfile
import time
import os
from dateutil.parser import parse
from dateutil import tz

from watchdog import estimators
from watchdog.misc import Message


class TestEstimator():
    def test___call__(monkeypatch):
        with pytest.raises(NotImplementedError):
            estimator = estimators.Estimator()
            estimator(None)


class TestSimpleEstimator():
    def test_inheritance(monkeypatch):
        estimator = estimators.SimpleEstimator()
        assert isinstance(estimator, estimators.Estimator)

    def describe___call__():
        def normal_case():
            estimator = estimators.SimpleEstimator()

            trigger_time = parse('2017/10/05T11:11:11Z')
            message = Message(trigger_time, 10, 1, 2)
            assert estimator(message) == None

            trigger_time = trigger_time + timedelta(seconds=1)
            message = Message(trigger_time, 15, 1, 2)
            assert estimator(message) == trigger_time + timedelta(seconds=7.5)

            trigger_time = trigger_time + timedelta(seconds=2)
            message = Message(trigger_time, 17, 1, 2)
            assert estimator(message) == trigger_time + timedelta(seconds=5.25)

        def with_factor():
            estimator = estimators.SimpleEstimator(factor=10)

            trigger_time = parse('2017/10/05T11:11:11Z')
            message = Message(trigger_time, 10, 1, 2)
            assert estimator(message) == None

            trigger_time = trigger_time + timedelta(seconds=1)
            message = Message(trigger_time, 15, 1, 2)
            assert estimator(message) == trigger_time + timedelta(seconds=50)

            trigger_time = trigger_time + timedelta(seconds=2)
            message = Message(trigger_time, 17, 1, 2)
            assert estimator(message) == trigger_time + timedelta(seconds=35)


class TestStaticEstimator():
    def test_inheritance(monkeypatch):
        estimator = estimators.StaticEstimator(duration=5)
        assert isinstance(estimator, estimators.Estimator)

    def test___call__(monkeypatch):
        estimator = estimators.StaticEstimator(duration=5)
        trigger_time = parse('2017/10/05T11:11:11Z')

        message = Message(trigger_time, 15, 1, 2)
        assert estimator(message) == trigger_time + timedelta(seconds=5)

        trigger_time = trigger_time + timedelta(seconds=1)
        message = Message(trigger_time, 17, 1, 2)
        assert estimator(message) == trigger_time + timedelta(seconds=5)
