import os

from setuptools import setup, find_packages


REQUIRES = []
with open('requirements.txt') as f:
    for line in f:
        line, _, _ = line.partition('#')
        line = line.strip()
        REQUIRES.append(line)

with open('test-requirements.txt') as f:
    TESTS_REQUIRES = f.readlines()


name = 'chainer-watchdog'
version_ns = {}
with open(os.path.join(os.path.dirname(__file__), 'watchdog', '_version.py')) as f:
    exec(f.read(), {}, version_ns)
version = version_ns['__version__']
release = version

setup(
    name=name,
    version=version,
    description='Watchdog extension for Chainer',
    url='https://github.com/dtaniwaki/chainer-watchdog',
    author='Daisuke Taniwaki',
    author_email='daisuketaniwaki@gmail.com',
    license='MIT',
    keywords='chainer extension',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=REQUIRES,
    tests_require=TESTS_REQUIRES,
    extras_require={
        'dev': [
            'pytest-runner>=2.0,<3dev',
            'tox>=2.7,<3dev',
            'detox>=0.11,<1dev',
            'bumpversion>=0.5.3,<1dev',
        ],
        'test': TESTS_REQUIRES,
        'lint': [
            'flake8>=3.5.0,<4dev',
            'flake8-blind-except>=0.1.1,<1dev',
            'flake8-import-order>=0.16,<1dev',
            'flake8-html>=0.4.0,<1dev',
            'autopep8>=1.3,<2dev',
            'autoflake>=1.1,<2dev',
            'mypy>=0.580,<1dev',
        ],
        'docs': [
            'sphinx>=1.7.1,<1.8dev',
            'sphinx_rtd_theme>=0.2.4,<0.3dev',
            'sphinxcontrib-blockdiag>=1.5.5,<1.6dev',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
