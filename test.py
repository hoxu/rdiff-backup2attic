#!/usr/bin/env python3
import os
import shutil
import subprocess
import tempfile
import unittest

import rb2a

def setUpModule():
    print('Creating fixture...')
    global tempdir, testdata, rdiffrepo
    tempdir = tempfile.mkdtemp('rb2a_unittest')

    # first rdiff-backup increment
    testdata = os.path.join(tempdir, 'testdata')
    os.mkdir(testdata)
    with open(os.path.join(testdata, 'data'), 'w') as f:
        f.write('first')

    rdiffrepo = os.path.join(tempdir, 'rdiff-repo')
    subprocess.check_call(['faketime', '2015-10-01 08:00:00', 'rdiff-backup', testdata, rdiffrepo])

    # second rdiff-backup increment
    with open(os.path.join(testdata, 'data'), 'w') as f:
        f.write('second')

    subprocess.check_call(['faketime', '2015-10-01 09:00:00', 'rdiff-backup', testdata, rdiffrepo])
    print('OK')

def tearDownModule():
    global tempdir
    shutil.rmtree(tempdir)

class TestRB2A(unittest.TestCase):
    def test_rdiff_parse(self):
        lines = """Found 1 increments:
    increments.2015-09-17T18:44:09+03:00.dir   Thu Sep 17 18:44:09 2015
Current mirror: Thu Sep 17 18:45:04 2015""".split('\n')
        increments = rb2a.parse_rdiff_increments(lines)
        self.assertEqual(len(increments), 2)
        self.assertEqual(increments[0], '2015-09-17T18:44:09')
        self.assertEqual(increments[1], '2015-09-17T18:45:04')

    def test_attic_parse(self):
        lines = """2015-09-17T18:44:09                  Sun Sep 20 13:58:44 2015
2015-09-17T18:45:04                  Sun Sep 20 14:02:40 2015""".split('\n')
        archives = rb2a.parse_attic_archives(lines)
        self.assertEqual(len(archives), 2)
        self.assertEqual(archives[0], '2015-09-17T18:44:09')
        self.assertEqual(archives[1], '2015-09-17T18:45:04')

    def test_get_increments_to_convert(self):
        increments = ['2015-10-01T08:00:00', '2015-10-01T09:00:00']
        archives = ['2015-10-01T09:00:00']
        results = rb2a.get_increments_to_convert(increments, archives)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], '2015-10-01T08:00:00')

    # integration tests below
    def test_parse_rdiff_repo(self):
        increments = rb2a.parse_rdiff_repo(rdiffrepo)
        self.assertEqual(len(increments), 2)
        # second can wary, depending on how long rdiff-backup takes to start up
        self.assertEqual(increments[0][:16], '2015-10-01T08:00')
        self.assertEqual(increments[1][:16], '2015-10-01T09:00')

    # TODO check logic for choosing increment->archive conversion
    # TODO integration test: create testdata, rdiff-backup repo, attic repository
    # TODO   test rdiff-backup -l
    # TODO   test attic list
    # TODO   test conversion of one backup

if __name__ == '__main__':
    unittest.main()
