#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='mqtt_videocap',
    version='0.0.1',
    description="Video capture service using ffmpeg, triggered by MQTT messages.",
    long_description=readme + '\n\n' + history,
    author="Ellis Percival",
    author_email='mqtt-videocap@failcode.co.uk',
    url='https://github.com/flyte/mqtt_videocap',
    packages=[
        'mqtt_videocap',
    ],
    package_dir={'mqtt_videocap':
                 'mqtt_videocap'},
    entry_points={
        'console_scripts': [
            'mqtt_videocap=mqtt_videocap.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='mqtt_videocap',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
