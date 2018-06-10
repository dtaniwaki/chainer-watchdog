import logging
import os
import signal

from .misc import SimpleFormatter

logger = logging.getLogger(__name__)


class Action(object):
    """Base class of watchdog action."""

    def __call__(self, tick_time, estimated_trigger_time, message):
        """Abstract method to execute.

        Args:
            tick_time (datetime) : Time of tick.
            estimated_trigger_time (datetime) : Estimated time of next trigger.
            message (Message) : Message received from a trainig process.
        """

        raise NotImplementedError()


class MessageAction(Action):
    _default_message_template = "Next trigger didn't come " \
                                "before the estimated time {estimated_trigger_time} " \
                                "since {last_trigger_time} " \
                                "at (epoch: {last_epoch_detail}, iteration: {last_iteration})."
    """Abstract watchdog action to emits a message to somewhere.

    Args:
        message_template (str) : Teamplte string of a message.
        tzinfo (tzinfo) : Timezone info to format datetime objects.
        formatter (function) : Function to format objects.
    """

    def __init__(self, message_template=_default_message_template, tzinfo=None, formatter=None):
        self._message_template = message_template
        self._formatter = formatter or SimpleFormatter(tzinfo=tzinfo)

    def _get_message(self, tick_time, estimated_trigger_time, message):
        kwargs = {
            'tick_time': tick_time,
            'estimated_trigger_time': estimated_trigger_time,
            'last_trigger_time': message.trigger_time,
            'last_iteration': message.iteration,
            'last_epoch_detail': message.epoch_detail,
        }
        for k, v in kwargs.items():
            kwargs[k] = self._formatter(k, v)
        return self._message_template.format(**kwargs)


class Abort(Action):
    """ Watchdog action to abort a training process.

    Args:
        pid (int) : PID of stopping process. Defaults to `os.getpid()`.
        signal (signals.signal, optional) : Signal to send to the process. Defaults to `signal.SIGTERM`.
    """

    def __init__(self, pid=os.getpid(), signal=signal.SIGTERM):
        self._pid = pid
        self._signal = signal

    def __call__(self, tick_time, estimated_trigger_time, message):
        os.kill(self._pid, self._signal)


class WarningMessage(MessageAction):
    """Watchdog action to log a message.

    Args:
        logger (logging.Logger, optional) : Logger instance to log. Defaults to the logger of this package.
    """

    def __init__(self, logger=logger, **kwargs):
        super(WarningMessage, self).__init__(**kwargs)

        self._logger = logger

    def __call__(self, tick_time, estimated_trigger_time, message):
        self._logger.warn(self._get_message(tick_time, estimated_trigger_time, message))


class SlackWebhookNotification(MessageAction):
    """Watchdog action to notify to a Slack channel by an incoming webhook.

    See https://api.slack.com/incoming-webhooks for more detail.

    Args:
        url (str) : URL string of an incoming webhook.
        channel (str) : Channel name with `#` prefix or user name with `@` prefix.
    """

    def __init__(self, url, channel, **kwargs):
        super(SlackWebhookNotification, self).__init__(**kwargs)

        try:
            from slackweb import Slack
        except ImportError as e:
            logger.error('You must insatll `slackweb` package to take this action.')
            raise e
        self._slack = Slack(url=url)
        self._channel = channel

    def __call__(self, tick_time, estimated_trigger_time, message):
        self._slack.notify(
            channel=self._channel,
            text=self._get_message(tick_time, estimated_trigger_time, message)
        )


class SlackNotification(MessageAction):
    """Watchdog action to notify to a Slack channel with an access token.

    See https://api.slack.com/custom-integrations/legacy-tokens for more detail.

    You can get your token from https://api.slack.com/custom-integrations/legacy-tokens .

    Args:
        token (str) : Slack access token.
        channel (str) : Channel name with `#` prefix or user name with `@` prefix.
    """

    def __init__(self, token, channel, **kwargs):
        super(SlackNotification, self).__init__(**kwargs)

        try:
            from slackclient import SlackClient
        except ImportError as e:
            logger.error('You must insatll `slackclient` package to take this action.')
            raise e
        self._slack = SlackClient(token)
        self._channel = channel

    def __call__(self, tick_time, estimated_trigger_time, message):
        self._slack.api_call(
            'chat.postMessage',
            channel=self._channel,
            text=self._get_message(tick_time, estimated_trigger_time, message)
        )
