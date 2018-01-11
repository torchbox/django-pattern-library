#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

import coverage

if __name__ == "__main__":
    cov = coverage.Coverage()
    cov.start()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    cov.stop()
    cov.save()
    cov.html_report()
    sys.exit(bool(failures))
