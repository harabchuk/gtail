import os
from setuptools import setup

from gtail import __version__


def main():
    cwd = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(cwd, 'README.md')
    readme = open(path, 'r').read()

    setup(
        name = 'gtail',
        version = __version__,
        description = 'Command line utility for sending log files to GrayLog2.',
        license = 'MIT',
        author = 'Aliaksei Harabchuk',
        author_email = 'aliaksei.harabchuk@gmail.com',
        keywords = ['logging', 'tail', 'graylog2'],
        url = 'https://github.com/harabchuk/gtail',
        packages = ['gtail'],
        entry_points = {
            'console_scripts': ['gtail=gtail.core:main']
        },
        test_suite='gtail.test',
        classifiers = [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License (MIT)",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Unix",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: System :: Logging"
            ],
        long_description = readme
    )


if __name__ == '__main__':
    main()
