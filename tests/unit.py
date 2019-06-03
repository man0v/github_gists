#!/usr/bin/env python

import unittest
import os
import sys
from datetime import datetime
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import github_gists as gg

class Test_Github_Gists(unittest.TestCase):
    """Unit tests for Github Gists"""

    def setUp(self):
        """Setup method for all tests"""

        # Remove last_check file
        try:
            os.remove('last_check')
        except FileNotFoundError:
            pass

    def test_set_time(self):
        """Test if we can set time to now or to zero"""

        dt = str(datetime.now().date())

        test_cases = (
            (True, dt),
            (False, '1970-01-01')
        )

        for x in test_cases:
            with self.subTest(x=x):
                ret = gg.set_time(x[0])
                self.assertTrue(ret.startswith(x[1]))

    def test_set_time_custom_file(self):
        """Test if set_time can work with another path to last_check"""

        test_str = '1970-01-01'

        with tempfile.NamedTemporaryFile() as tmp_file:
            ret = gg.set_time(False, tmp_file.name)
            self.assertTrue(ret.startswith(test_str))

            tmp_file.seek(0)
            tmp_file_content = tmp_file.read().decode()
            self.assertTrue(tmp_file_content.startswith(test_str))

    def test_set_time_bad_file(self):
        """Test what happens when bad path is passed"""

        test_cases = (
            '/root/.bash_history',
            '/asd'
        )

        for x in test_cases:
            with self.subTest(x=x):
                with self.assertRaises(SystemExit) as context:
                    ret = gg.set_time(True, x)

                self.assertEqual(context.exception.code, 1)

        with tempfile.NamedTemporaryFile() as tmp_file:
            os.chmod(tmp_file.name, 0o000)

            with self.assertRaises(SystemExit) as context:
                ret = gg.set_time(True, tmp_file.name)

            self.assertEqual(context.exception.code, 1)

    def test_get_time_return(self):
        """Test get_time returns string"""

        with open("last_check", 'w') as fn:
            fn.write('test')

        self.assertIsInstance(gg.get_time(), str)
        self.assertEqual(gg.get_time(), "test")

        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.write(b'test')
            tmp_file.seek(0)

            self.assertEqual(gg.get_time(tmp_file.name), 'test')


    def test_get_time_bad_file(self):
        """Test get_time exits when a bad path is passed"""

        test_cases = (
            '/root/.bash_history',
            '/'
        )

        for x in test_cases:
            with self.subTest(x=x):
                with self.assertRaises(SystemExit) as context:
                    gg.get_time(x)

                self.assertEqual(context.exception.code, 1)

    def test_get_gists_returns(self):
        """Test get_gists returns expected values"""

        iso = lambda x: datetime.fromisoformat(x).isoformat()

        username = 'geerlingguy'

        test_cases = (
            (iso('1970-01-01'), 28),
            (iso('2017-06-29'), 16),
            (iso('2018-03-04'), 11),
            (iso('2018-12-13'), 8),
            (iso('2019-02-25'), 7),
            (iso('2019-05-05'), 2)
        )

        for t in test_cases:
            with self.subTest(x = t[0], y = t[1]):
                ret = gg.get_gists(t[0], username)
                self.assertEqual(ret, t[1])

    def test_is_iso8601(self):
        """Test is_is8601 with various strings"""

        true_cases = (
            '1970-01-01T00:00:00Z',
            '1970-01-01T00:00:00',
            '2010-05-10T01:45:36.123Z',
            '2009-12-24T15:46:24Z'
        )

        for x in true_cases:
            with self.subTest(x=x):
                self.assertTrue(gg.is_iso8601(x))

        false_cases = (
            '1970-01-01',
            '1970-01-01T00:00:00Y',
            '1970-01-01T30:00:00',
            '2010-05-10T01:45:66.123Z',
            '2010-15-10T01:45:36.123Z',
            '2009-12-34T15:46:24Z'
            '2009-12-14T22:46:24Z'
        )

        for x in false_cases:
            with self.subTest(x=x):
                self.assertFalse(gg.is_iso8601(x))


if __name__ == '__main__':
    unittest.main(warnings='ignore')
