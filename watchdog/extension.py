import time
from datetime import datetime
from multiprocessing import Event, Process, Queue

from chainer.training import extension, trigger as trigger_module

from dateutil import tz

from six.moves.queue import Empty

from .misc import Message, WatchItem


class Watchdog(extension.Extension):
    """Trainer extension of Watchdog.

    This extension monitors training progress and execute watching items.

    Args:
        watch_items (list[tuple(Action, Estimator)]) : Items to watch.
        trigger (tuple, optional) : Defaults to `(100, 'iteration')`.
        interval (float, optional) : Interval (seconds) to check the state. Defaults to `5.0`.
    """

    def __init__(self, watch_items, trigger=(100, 'iteration'), interval=5.0):
        self._trigger = trigger_module.get_trigger(trigger)
        self._interval = interval
        self._watch_items = []
        for item in watch_items:
            if not isinstance(item, WatchItem):
                action, estimator = item
                item = WatchItem(action=action, estimator=estimator)
            self._watch_items.append(item)

        self._heartbeat_queue = Queue()
        self._stop_event = Event()
        self._heartbeat_thread = Process(target=self._heartbeat_handler)
        self._heartbeat_thread.daemon = True

    def initialize(self, trainer):
        self._trigger(trainer)
        self._heartbeat_thread.start()

    def __call__(self, trainer):
        if not self._heartbeat_thread.is_alive():
            raise RuntimeError('Heartbeat thread is dead')

        if self._trigger(trainer):
            message = Message(datetime.now(tz.tzutc()), trainer.elapsed_time,
                              trainer.updater.epoch_detail, trainer.updater.iteration)
            self._heartbeat_queue.put_nowait(message)

    def finalize(self):
        self._stop_event.set()
        if self._heartbeat_thread.is_alive():
            self._heartbeat_thread.join()

    def _heartbeat_handler(self):
        while not self._stop_event.is_set():
            message = None
            tick_time = datetime.now(tz.tzutc())
            try:
                message = self._heartbeat_queue.get_nowait()
            except Empty:
                pass
            for watch_item in self._watch_items:
                watch_item(tick_time, message)
            if not self._stop_event.is_set():
                time.sleep(self._interval)
