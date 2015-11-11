#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
    'configargparse',
    'simplejson',
    'gitpython'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='yolo',
    version='0.0.0',
    description="yolo, sorry.",
    long_description=readme + '\n\n' + history,
    author="Tom Neyland",
    author_email='tcneyland@gmail.com',
    url='https://github.com/TomNeyland/yolo',
    packages=[
        'yolo',
    ],
    package_dir={'yolo':
                 'yolo'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='yolo',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            'yolo=yolo.yolo:main'
        ],
    },
)
