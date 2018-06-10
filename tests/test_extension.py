import pytest
try:
    import mock
except ImportError:
    from unittest import mock
from datetime import datetime, timedelta
import tempfile

from chainer import training

from watchdog import extension as watchdog_extension
from watchdog.misc import WatchItem


def get_trainer():
    trainer = lambda: None
    trainer.out = tempfile.gettempprefix()
    trainer.serialize = lambda x: None
    trainer.elapsed_time = 100
    trainer.updater = lambda: None
    trainer.updater.epoch_detail = 0.5
    trainer.updater.iteration = 0.5
    return trainer


class TestWatchdog():
    def test_inheritance(monkeypatch):
        extension = watchdog_extension.Watchdog(watch_items=[])
        assert isinstance(extension, training.extension.Extension)

    def describe___init__():
        def test_with_watch_items():
            extension = watchdog_extension.Watchdog(watch_items=[('action', 'estimator')])
            assert [type(item) for item in extension._watch_items] == [watchdog_extension.WatchItem]

        def test_with_tuple_watch_items():
            extension = watchdog_extension.Watchdog(watch_items=[watchdog_extension.WatchItem('action', 'estimator')])
            assert [type(item) for item in extension._watch_items] == [watchdog_extension.WatchItem]

    def describe_initialize():
        def start_heartbeat_thread():
            trainer = get_trainer()
            extension = watchdog_extension.Watchdog(watch_items=[])

            assert not extension._heartbeat_thread.is_alive()
            extension.initialize(trainer)
            assert extension._heartbeat_thread.is_alive()

    def describe___call__():
        def with_trigger():
            trainer = get_trainer()
            extension = watchdog_extension.Watchdog(watch_items=[], trigger=lambda trainer: True)
            extension.initialize(trainer)
            extension(trainer)

        def without_trigger():
            trainer = get_trainer()
            extension = watchdog_extension.Watchdog(watch_items=[], trigger=lambda trainer: False)
            extension.initialize(trainer)
            extension(trainer)

        def on_dead_heartbeat_thread():
            trainer = get_trainer()
            extension = watchdog_extension.Watchdog(watch_items=[])
            with pytest.raises(RuntimeError) as exc_info:
                extension(trainer)
            assert str(exc_info.value) == 'Heartbeat thread is dead'

    def describe_finalize():
        def shutdown_heartbeat_thread():
            trainer = get_trainer()
            extension = watchdog_extension.Watchdog(watch_items=[])
            extension.initialize(trainer)

            assert extension._heartbeat_thread.is_alive()
            extension.finalize()
            assert not extension._heartbeat_thread.is_alive()


