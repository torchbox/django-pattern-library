#!/usr/bin/env python
import argparse
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

import coverage

parser = argparse.ArgumentParser()
parser.add_argument(
    '-v', '--verbosity', action='store', dest='verbosity', default=1,
    type=int, choices=range(4),
    help="Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output",
)

if __name__ == "__main__":
    # Coverage setup
    cov = coverage.Coverage()
    cov.start()

    # Django setup
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings.dev'
    django.setup()

    # Test runner setup
    TestRunner = get_runner(settings)
    TestRunner.add_arguments(parser)
    args = parser.parse_args()
    test_runner = TestRunner(**vars(args))
    failures = test_runner.run_tests(["tests"])

    # Generate coverage report
    cov.stop()
    cov.save()
    cov.html_report()

    sys.exit(bool(failures))
