**[Prerequisites](#prerequisites)** |
**[Installation](#installation)** |
**[Usage](#usage)** |
**[Development](#development)** |
**[Test](#test)** |
**[Contributing](#contributing)** |
**[License](#license)** |

# chainer-watchdog

[![PyPI][pypi-image]][pypi-link]
[![GitHub license][license-image]][license-link]
[![PyVersions][pyversions-image]][pypi-link]
[![Build Status][build-image]][build-link]
[![codecov][cov-image]][cov-link]

This Python package provides watchdog functions for Chainer.

## Prerequisites

Python 2.7, 3.4, 3.5, 3.6.

## Installation

Install chainer-watchdog to the system:

```sh
pip install chainer-watchdog
```

## Installation from GitHub

```sh
git clone https://github.com/dtaniwaki/chainer-watchdog
cd chainer-watchdog
python setup.py install
```

or use pip.

```sh
pip install git+https://github.com/dtaniwaki/chainer-watchdog.git
```

## Usage

Extend your Chainer trainer with this extension. You can make any combination of an action and an estimator. See [actions](watchdog/actions.py) and [estimators](watchdog/estimators.py) for available watchdog items.

```python
from watchdog import WatchDog
from watchdog.estimators import SimpleEstimator, StaticEstimator
from watchdog.actions import Abort, WarningMessage, SlackNotification

slack_token = os.environ['SLACK_TOKEN']
slack_channel = os.environ['SLACK_CHANNEL']

trainer.extend(WatchDog(watch_items=[
    (WarningMessage(), SimpleEstimator(factor=2.0)),
    (SlackNotification(
        token=slack_token,
        channel=slack_channel,
    ), SimpleEstimator(factor=3.0)),
    (Abort(), StaticEstimator(duration=60)),
]))
```

With this example code, the training process will show warning message if training speed becomes 2 times slower than usual. Then, it will notify you in Slack if training speed becomes 3 times slower than usual. Finally, it will terminate your training process if it doesn't get any update for 60 seconds.

## Development

```sh
$ pip install -e .[dev]
```

## Documentation

Generate the documentation.

```sh
$ pip install -e .[docs]
$ sphinx-apidoc -f -o docs/source/ watchdog
$ make -C docs -f Makefile html
```

You can check the generate docs by:

```sh
$ open docs/_build/html/index.html
```

## Test

```sh
$ pip install -e .[test]
$ pytest
```

You can check the test coverage as HTML by:

```sh
$ open htmlcov/index.html
```

Or use `tox` to test this package in multiple python versions.

```sh
$ tox
```

Run all the Python version tests in parallel,

```sh
$ detox
```


### Lint

Lint the source code.

```sh
$ pip install -e .[lint]
$ python setup.py flake8
$ open htmlflake8/index.html
```

### Type Check

```sh
$ mypy --py2 watchdog
```

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new [Pull Request](../../pull/new/master)

## Copyright

Copyright (c) 2018 Daisuke Taniwaki. See [LICENSE](LICENSE) for details.


[pypi-image]:  https://img.shields.io/pypi/v/chainer-watchdog.svg
[pypi-link]:   https://pypi.python.org/pypi/chainer-watchdog
[license-image]: https://img.shields.io/github/license/dtaniwaki/chainer-watchdog.svg
[license-link]:  https://github.com/dtaniwaki/chainer-watchdog
[pyversions-image]: https://img.shields.io/pypi/pyversions/chainer-watchdog.svg
[build-image]: https://travis-ci.org/dtaniwaki/chainer-watchdog.svg
[build-link]:  https://travis-ci.org/dtaniwaki/chainer-watchdog
[cov-image]:   https://codecov.io/gh/dtaniwaki/chainer-watchdog/branch/master/graph/badge.svg
[cov-link]:    https://codecov.io/gh/dtaniwaki/chainer-watchdog
