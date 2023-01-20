# -*- coding: utf-8 -*-

import arabic_reshaper
import arabic_reshaper.ligatures as ligatures
import itertools
import sys
import unittest


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
        config = {}
        for l in itertools.chain(ligatures.SENTENCES_LIGATURES, ligatures.WORDS_LIGATURES, ligatures.LETTERS_LIGATURES):
            config[l[0]] = True
        self.reshaper = arabic_reshaper.ArabicReshaper(config)
        self.cases = (
            ('\u0645\u064A\u0646','\uFEE3\uFC94'),
        )

    def test_reshaping(self):
        _reshaping_test(self)


if __name__ == '__main__':
    unittest.main()
