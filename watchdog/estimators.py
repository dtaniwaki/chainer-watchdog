from datetime import timedelta


class Estimator(object):
    """Base class to estimate next trigger time."""

    def __call__(self, message):
        """Abstract method to estimate next trigger time.

        Args:
            message: (Message) : Message received from a training process.
        """

        raise NotImplementedError()


class SimpleEstimator(Estimator):
    """Estimator which estimate next trigger time based on the speed of training.

    Args:
        factor (float, optional) : Factor to multiply the speed. Defaults to `1.5`.
    """

    def __init__(self, factor=1.5):
        self._factor = factor
        self._start_message = None
        self._count = 0

    def __call__(self, message):
        if self._count == 0:
            self._start_message = message
            estimated_time = None
        else:
            diff = message.elapsed_time - self._start_message.elapsed_time
            estimated_time = message.trigger_time + timedelta(seconds=self._factor * diff / self._count)

        self._count = self._count + 1
        return estimated_time


class StaticEstimator(Estimator):
    """Estimator which estimate next trigger time with a fixed duration.

    Args:
        duration (float) : Duration (seconds) to estimate next trigger time.
    """

    def __init__(self, duration):
        self._duration = duration

    def __call__(self, message):
        return message.trigger_time + timedelta(seconds=self._duration)
