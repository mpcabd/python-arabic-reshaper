# -*- coding: utf-8 -*-

import unittest
import sys
import arabic_reshaper
import arabic_reshaper.letters as letters


def _reshaping_test(test):
    for i, case in enumerate(test.cases):
        def t(): test.assertEqual(case[1], test.reshaper.reshape(case[0]))
        if hasattr(test, 'subTest'):
            with test.subTest(i=i, case=case[0]):

                t()
        else:
            print('running test case %d' % i, file=sys.stderr)
            t()


class TestDefaultReshaping(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.default_reshaper
        self.cases = (
            ('چۆمان','ﭼﯚﻣﺎﻥ'),
            ('گۆیژە','ﮔﯚﯾﮋە'),
            ('ﺧﯚﻣﺎﻥ ﺧﯚﺵ','ﺧﯚﻣﺎﻥ ﺧﯚﺵ'),


        )
        print(self.cases[0][0])

    def test_reshaping(self):
        _reshaping_test(self)




if __name__ == '__main__':
    unittest.main()
