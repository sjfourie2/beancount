"""Tests for file utilities.
"""
__author__ = "Martin Blais <blais@furius.ca>"

from os import path
import io
import os
import re
import unittest

from beancount.utils import test_utils
from beancount.utils import file_utils


def clean(prefix, iterable):
    return [re.sub('^{}/'.format(re.escape(prefix)), '', f)
            for f in iterable]


class TestFileUtilsFind(test_utils.TestTempdirMixin, test_utils.TestCase):

    def setUp(self):
        super().setUp()
        for filename in [
                'alice/',
                'alice/bottle.txt',
                'rabbit/',
                'rabbit/suit/',
                'rabbit/suit/glasses.txt',
                'caterpillar/',
                'caterpillar/who-are-you.txt',
                ]:
            abs_filename = path.join(self.tempdir, filename)
            if filename.endswith('/'):
                os.makedirs(abs_filename)
            else:
                open(abs_filename, 'w').close()

    def test_find_files(self):
        def walk(fords):
            return clean(self.tempdir, file_utils.find_files(fords))

        self.assertEqual(['alice/bottle.txt',
                          'rabbit/suit/glasses.txt',
                          'caterpillar/who-are-you.txt'],
                         walk([self.tempdir]))

        self.assertEqual(['alice/bottle.txt'],
                         walk([path.join(self.tempdir, 'alice/bottle.txt')]))

        self.assertEqual([],
                         walk([path.join(self.tempdir, 'alice/blabla.txt')]))

        # Test a string directly.
        self.assertEqual(['alice/bottle.txt'],
                         walk(path.join(self.tempdir, 'alice/bottle.txt')))


class TestMiscFileUtils(unittest.TestCase):

    def test_guess_file_format(self):
        self.assertEqual('csv', file_utils.guess_file_format('/user/output.csv'))
        self.assertEqual('text', file_utils.guess_file_format('/user/output.text'))
        self.assertEqual('text', file_utils.guess_file_format('/user/output.txt'))
        self.assertEqual('html', file_utils.guess_file_format('/user/output.html'))
        self.assertEqual('html', file_utils.guess_file_format('/user/output.xhtml'))
        self.assertEqual(None, file_utils.guess_file_format('/user/output'))

    def test_path_greedy_split(self):
        self.assertEqual(('/tmp/tmp.ju3h4h/blabla', None),
                         file_utils.path_greedy_split('/tmp/tmp.ju3h4h/blabla'))
        self.assertEqual(('/tmp/tmp.ju3h4h/bla', '.tgz'),
                         file_utils.path_greedy_split('/tmp/tmp.ju3h4h/bla.tgz'))
        self.assertEqual(('/tmp/tmp.ju3h4h/bla', '.tar.gz'),
                         file_utils.path_greedy_split('/tmp/tmp.ju3h4h/bla.tar.gz'))
