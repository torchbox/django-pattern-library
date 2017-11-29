#!/usr/bin/env python

from setuptools import find_packages, setup

from pattern_library import __version__

setup(
    name='django-pattern-library',
    version=__version__,
    description='A module for Django that allows to build pattern libraries for your projects.',
    author='Mikalai Radchuk',
    author_email='mikalai.radchuk@torchbox.com',
    url='https://github.com/torchbox/django-pattern-library',
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    long_description='See https://github.com/torchbox/django-pattern-library for details',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
    ],
    install_requires=[
        'Django>=1.11',
    ],
    zip_safe=False,
)
