#!/usr/bin/env python

from setuptools import find_packages, setup

from pattern_library import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-pattern-library',
    version=__version__,
    description='A module for Django that allows to build pattern libraries for your projects.',
    author='Mikalai Radchuk',
    author_email='mikalai.radchuk@torchbox.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    license='BSD',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
        'PyYAML>=5.1',
    ],
    extras_require={
        'dev': [
            'beautifulsoup4',
            'coverage',
            'flake8==3.7.7',
            'isort==4.3.15',
        ],
    },
    zip_safe=False,
)
