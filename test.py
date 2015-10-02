#!/usr/bin/env python3
import unittest

import rb2a

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

    # TODO check logic for choosing increment->archive conversion
    # TODO integration test: create testdata, rdiff-backup repo, attic repository
    # TODO   test rdiff-backup -l
    # TODO   test attic list
    # TODO   test conversion of one backup

if __name__ == '__main__':
    unittest.main()
