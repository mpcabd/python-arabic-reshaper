# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import arabic_reshaper


class TestDefaultReshaping(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.default_reshaper
        self.cases = (
            ('السلام عليكم', 'ﺍﻟﺴﻼﻡ ﻋﻠﻴﻜﻢ'),
            ('السَلَاْمٌ عَلَيْكُمْ', 'ﺍﻟﺴﻼﻡ ﻋﻠﻴﻜﻢ'),
        )

    def test_reshaping(self):
        for i, case in enumerate(self.cases):
            if hasattr(self, 'subTest'):
                with self.subTest(i=i, case=case[0]):
                    self.assertEqual(case[1], self.reshaper.reshape(case[0]))
            else:
                self.assertEqual(case[1], self.reshaper.reshape(case[0]))


class TestReshapingWithHarakat(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.ArabicReshaper({
            'delete_harakat': False
        })
        self.cases = (
            ('السَلَاْمٌ عَلَيْكُمْ', 'ﺍﻟﺴَﻼَْﻡٌ ﻋَﻠَﻴْﻜُﻢْ'),
        )

    def test_reshaping(self):
        for i, case in enumerate(self.cases):
            if hasattr(self, 'subTest'):
                with self.subTest(i=i, case=case[0]):
                    self.assertEqual(case[1], self.reshaper.reshape(case[0]))
            else:
                self.assertEqual(case[1], self.reshaper.reshape(case[0]))

if __name__ == '__main__':
    unittest.main()
