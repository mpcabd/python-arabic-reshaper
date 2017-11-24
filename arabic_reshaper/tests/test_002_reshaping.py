# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

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
            ('السلام عليكم', 'ﺍﻟﺴﻼﻡ ﻋﻠﻴﻜﻢ'),
            ('السَلَاْمٌ عَلَيْكُمْ', 'ﺍﻟﺴﻼﻡ ﻋﻠﻴﻜﻢ'),
            ('اللغة العربية هي أكثر اللغات', 'ﺍﻟﻠﻐﺔ ﺍﻟﻌﺮﺑﻴﺔ ﻫﻲ ﺃﻛﺜﺮ ﺍﻟﻠﻐﺎﺕ'),
            ('تحدثاً ونطقاً ضمن مجموعة', 'ﺗﺤﺪﺛﺎ ﻭﻧﻄﻘﺎ ﺿﻤﻦ ﻣﺠﻤﻮﻋﺔ'),
            ('اللغات السامية', 'ﺍﻟﻠﻐﺎﺕ ﺍﻟﺴﺎﻣﻴﺔ'),
            ('العربية لغة رسمية في',  'ﺍﻟﻌﺮﺑﻴﺔ ﻟﻐﺔ ﺭﺳﻤﻴﺔ ﻓﻲ'),
            ('كل دول الوطن العربي',  'ﻛﻞ ﺩﻭﻝ ﺍﻟﻮﻃﻦ ﺍﻟﻌﺮﺑﻲ'),
            ('إضافة إلى كونها لغة',  'ﺇﺿﺎﻓﺔ ﺇﻟﻰ ﻛﻮﻧﻬﺎ ﻟﻐﺔ'),
            ('رسمية في تشاد وإريتريا',  'ﺭﺳﻤﻴﺔ ﻓﻲ ﺗﺸﺎﺩ ﻭﺇﺭﻳﺘﺮﻳﺎ'),
            ('وإسرائيل. وهي إحدى اللغات',  'ﻭﺇﺳﺮﺍﺋﻴﻞ. ﻭﻫﻲ ﺇﺣﺪﻯ ﺍﻟﻠﻐﺎﺕ'),
            ('الرسمية الست في منظمة',  'ﺍﻟﺮﺳﻤﻴﺔ ﺍﻟﺴﺖ ﻓﻲ ﻣﻨﻈﻤﺔ'),
            ('الأمم المتحدة، ويُحتفل',  'ﺍﻷﻣﻢ ﺍﻟﻤﺘﺤﺪﺓ، ﻭﻳﺤﺘﻔﻞ'),
            ('باليوم العالمي للغة العربية',  'ﺑﺎﻟﻴﻮﻡ ﺍﻟﻌﺎﻟﻤﻲ ﻟﻠﻐﺔ ﺍﻟﻌﺮﺑﻴﺔ'),
            ('في 18 ديسمبر كذكرى اعتماد',  'ﻓﻲ 18 ﺩﻳﺴﻤﺒﺮ ﻛﺬﻛﺮﻯ ﺍﻋﺘﻤﺎﺩ'),
            ('العربية بين لغات العمل في',  'ﺍﻟﻌﺮﺑﻴﺔ ﺑﻴﻦ ﻟﻐﺎﺕ ﺍﻟﻌﻤﻞ ﻓﻲ'),
            ('الأمم المتحدة.', 'ﺍﻷﻣﻢ ﺍﻟﻤﺘﺤﺪﺓ.'),
        )

    def test_reshaping(self):
        _reshaping_test(self)


class TestZWJReshaping(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.default_reshaper

        BEH = 'ب'
        BEH_ISOLATED = letters.LETTERS[BEH][letters.ISOLATED]
        BEH_INITIAL = letters.LETTERS[BEH][letters.INITIAL]
        BEH_MEDIAL = letters.LETTERS[BEH][letters.MEDIAL]
        BEH_FINAL = letters.LETTERS[BEH][letters.FINAL]

        ALEF = 'ا'
        ALEF_ISOLATED = letters.LETTERS[ALEF][letters.ISOLATED]
        ALEF_FINAL = letters.LETTERS[ALEF][letters.FINAL]

        HAMZA = 'ء'
        HAMZA_ISOLATED = letters.LETTERS[HAMZA][letters.ISOLATED]

        self.cases = (
            (
                BEH + HAMZA,
                BEH_ISOLATED + HAMZA_ISOLATED
            ),
            (
                letters.ZWJ + BEH + HAMZA,
                BEH_FINAL + HAMZA_ISOLATED
            ),
            (
                letters.ZWJ + BEH,
                BEH_FINAL
            ),
            (
                BEH + letters.ZWJ,
                BEH_INITIAL
            ),
            (
                letters.ZWJ + BEH + letters.ZWJ,
                BEH_MEDIAL
            ),
            (
                BEH + letters.ZWJ + HAMZA,
                BEH_INITIAL + HAMZA_ISOLATED
            ),
            (
                BEH + ALEF,
                BEH_INITIAL + ALEF_FINAL
            ),
            (
                BEH + letters.ZWJ + ALEF,
                BEH_INITIAL + ALEF_FINAL
            ),
            (
                BEH + letters.ZWJ + ALEF + letters.ZWJ,
                BEH_INITIAL + ALEF_FINAL
            ),
            (
                BEH + ALEF + BEH,
                BEH_INITIAL + ALEF_FINAL + BEH_ISOLATED
            ),
            (
                BEH + letters.ZWJ + ALEF + letters.ZWJ + BEH,
                BEH_INITIAL + ALEF_FINAL + BEH_FINAL
            ),
            (
                BEH + letters.ZWJ + HAMZA + BEH,
                BEH_INITIAL + HAMZA_ISOLATED + BEH_ISOLATED
            ),
            (
                BEH + letters.ZWJ + HAMZA + letters.ZWJ + BEH,
                BEH_INITIAL + HAMZA_ISOLATED + BEH_FINAL
            ),
        )

    def test_reshaping(self):
        _reshaping_test(self)


class TestReshapingWithHarakat(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.ArabicReshaper({
            'delete_harakat': False
        })
        self.cases = (
            ('السَلَاْمٌ عَلَيْكُمْ', 'ﺍﻟﺴَﻼَْﻡٌ ﻋَﻠَﻴْﻜُﻢْ'),
            ('اللغة العربية هي أكثر اللغات', 'ﺍﻟﻠﻐﺔ ﺍﻟﻌﺮﺑﻴﺔ ﻫﻲ ﺃﻛﺜﺮ ﺍﻟﻠﻐﺎﺕ'),
            ('تحدثاً ونطقاً ضمن مجموعة', 'ﺗﺤﺪﺛﺎً ﻭﻧﻄﻘﺎً ﺿﻤﻦ ﻣﺠﻤﻮﻋﺔ'),
            ('اللغات السامية', 'ﺍﻟﻠﻐﺎﺕ ﺍﻟﺴﺎﻣﻴﺔ'),
            ('العربية لغة رسمية في',  'ﺍﻟﻌﺮﺑﻴﺔ ﻟﻐﺔ ﺭﺳﻤﻴﺔ ﻓﻲ'),
            ('كل دول الوطن العربي',  'ﻛﻞ ﺩﻭﻝ ﺍﻟﻮﻃﻦ ﺍﻟﻌﺮﺑﻲ'),
            ('إضافة إلى كونها لغة',  'ﺇﺿﺎﻓﺔ ﺇﻟﻰ ﻛﻮﻧﻬﺎ ﻟﻐﺔ'),
            ('رسمية في تشاد وإريتريا',  'ﺭﺳﻤﻴﺔ ﻓﻲ ﺗﺸﺎﺩ ﻭﺇﺭﻳﺘﺮﻳﺎ'),
            ('وإسرائيل. وهي إحدى اللغات',  'ﻭﺇﺳﺮﺍﺋﻴﻞ. ﻭﻫﻲ ﺇﺣﺪﻯ ﺍﻟﻠﻐﺎﺕ'),
            ('الرسمية الست في منظمة',  'ﺍﻟﺮﺳﻤﻴﺔ ﺍﻟﺴﺖ ﻓﻲ ﻣﻨﻈﻤﺔ'),
            ('الأمم المتحدة، ويُحتفل',  'ﺍﻷﻣﻢ ﺍﻟﻤﺘﺤﺪﺓ، ﻭﻳُﺤﺘﻔﻞ'),
            ('باليوم العالمي للغة العربية',  'ﺑﺎﻟﻴﻮﻡ ﺍﻟﻌﺎﻟﻤﻲ ﻟﻠﻐﺔ ﺍﻟﻌﺮﺑﻴﺔ'),
            ('في 18 ديسمبر كذكرى اعتماد',  'ﻓﻲ 18 ﺩﻳﺴﻤﺒﺮ ﻛﺬﻛﺮﻯ ﺍﻋﺘﻤﺎﺩ'),
            ('العربية بين لغات العمل في',  'ﺍﻟﻌﺮﺑﻴﺔ ﺑﻴﻦ ﻟﻐﺎﺕ ﺍﻟﻌﻤﻞ ﻓﻲ'),
            ('الأمم المتحدة.', 'ﺍﻷﻣﻢ ﺍﻟﻤﺘﺤﺪﺓ.'),
        )

    def test_reshaping(self):
        _reshaping_test(self)


class TestReshapingWithHarakatWithoutLigatures(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.ArabicReshaper({
            'delete_harakat': False,
            'support_ligatures': False
        })
        self.cases = (
            ('السَلَاْمٌ عَلَيْكُمْ', 'ﺍﻟﺴَﻠَﺎْﻡٌ ﻋَﻠَﻴْﻜُﻢْ'),
            ('اللغة العربية هي أكثر اللغات', 'ﺍﻟﻠﻐﺔ ﺍﻟﻌﺮﺑﻴﺔ ﻫﻲ ﺃﻛﺜﺮ ﺍﻟﻠﻐﺎﺕ'),
            ('تحدثاً ونطقاً ضمن مجموعة', 'ﺗﺤﺪﺛﺎً ﻭﻧﻄﻘﺎً ﺿﻤﻦ ﻣﺠﻤﻮﻋﺔ'),
            ('اللغات السامية', 'ﺍﻟﻠﻐﺎﺕ ﺍﻟﺴﺎﻣﻴﺔ'),
            ('العربية لغة رسمية في',  'ﺍﻟﻌﺮﺑﻴﺔ ﻟﻐﺔ ﺭﺳﻤﻴﺔ ﻓﻲ'),
            ('كل دول الوطن العربي',  'ﻛﻞ ﺩﻭﻝ ﺍﻟﻮﻃﻦ ﺍﻟﻌﺮﺑﻲ'),
            ('إضافة إلى كونها لغة',  'ﺇﺿﺎﻓﺔ ﺇﻟﻰ ﻛﻮﻧﻬﺎ ﻟﻐﺔ'),
            ('رسمية في تشاد وإريتريا',  'ﺭﺳﻤﻴﺔ ﻓﻲ ﺗﺸﺎﺩ ﻭﺇﺭﻳﺘﺮﻳﺎ'),
            ('وإسرائيل. وهي إحدى اللغات',  'ﻭﺇﺳﺮﺍﺋﻴﻞ. ﻭﻫﻲ ﺇﺣﺪﻯ ﺍﻟﻠﻐﺎﺕ'),
            ('الرسمية الست في منظمة',  'ﺍﻟﺮﺳﻤﻴﺔ ﺍﻟﺴﺖ ﻓﻲ ﻣﻨﻈﻤﺔ'),
            ('الأمم المتحدة، ويُحتفل',  'ﺍﻟﺄﻣﻢ ﺍﻟﻤﺘﺤﺪﺓ، ﻭﻳُﺤﺘﻔﻞ'),
            ('باليوم العالمي للغة العربية',  'ﺑﺎﻟﻴﻮﻡ ﺍﻟﻌﺎﻟﻤﻲ ﻟﻠﻐﺔ ﺍﻟﻌﺮﺑﻴﺔ'),
            ('في 18 ديسمبر كذكرى اعتماد',  'ﻓﻲ 18 ﺩﻳﺴﻤﺒﺮ ﻛﺬﻛﺮﻯ ﺍﻋﺘﻤﺎﺩ'),
            ('العربية بين لغات العمل في',  'ﺍﻟﻌﺮﺑﻴﺔ ﺑﻴﻦ ﻟﻐﺎﺕ ﺍﻟﻌﻤﻞ ﻓﻲ'),
            ('الأمم المتحدة.', 'ﺍﻟﺄﻣﻢ ﺍﻟﻤﺘﺤﺪﺓ.'),
        )

    def test_reshaping(self):
        _reshaping_test(self)


class TestReshapingWithShiftedHarakatWithoutLigatures(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.ArabicReshaper({
            'delete_harakat': False,
            'support_ligatures': False,
            'shift_harakat_position': True,
        })
        self.cases = (
            ('فُعِلَ', 'ُﻓِﻌَﻞ'),
            ('فُعِّلَ', 'ُﻓِّﻌَﻞ'),
        )

    def test_reshaping(self):
        _reshaping_test(self)


class TestReshapingSomeLigatures(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.ArabicReshaper({
            'delete_tatweel': True,
            'ARABIC LIGATURE BISMILLAH AR-RAHMAN AR-RAHEEM': True,
            'ARABIC LIGATURE JALLAJALALOUHOU': True,
            'ARABIC LIGATURE SALLALLAHOU ALAYHE WASALLAM': True,
            'ARABIC LIGATURE ALLAH ': True,
            'ARABIC LIGATURE AKBAR': True,
            'ARABIC LIGATURE ALAYHE': True,
            'ARABIC LIGATURE MOHAMMAD': True,
            'ARABIC LIGATURE RASOUL': True,
            'ARABIC LIGATURE SALAM': True,
            'ARABIC LIGATURE SALLA': True,
            'ARABIC LIGATURE WASALLAM': True,
        })
        self.cases = (
            ('إِنَّهُ مِن سُلَيْمَانَ '
             'وَإِنَّهُ بِسْمِ اللّـَهِ '
             'الرَّحْمَـٰنِ الرَّحِيمِ ﴿٣٠﴾ '
             'أَلَّا تَعْلُوا عَلَيَّ '
             'وَأْتُونِي مُسْلِمِينَ ﴿٣١﴾',

             'ﺇﻧﻪ ﻣﻦ ﺳﻠﻴﻤﺎﻥ ﻭﺇﻧﻪ ﷽ ﴿٣٠﴾ '
             'ﺃﻻ ﺗﻌﻠﻮﺍ ﻋﻠﻲ ﻭﺃﺗﻮﻧﻲ ﻣﺴﻠﻤﻴﻦ ﴿٣١﴾'),

            ('فَذَكِّرْ إِنَّمَا أَنتَ'
             ' مُذَكِّرٌ ﴿٢١﴾ لَّسْتَ'
             ' عَلَيْهِم بِمُصَيْطِرٍ ﴿٢٢﴾'
             ' إِلَّا مَن تَوَلَّىٰ'
             ' وَكَفَرَ ﴿٢٣﴾ فَيُعَذِّبُهُ'
             ' اللَّـهُ الْعَذَابَ'
             ' الْأَكْبَرَ ﴿٢٤﴾',

             'ﻓﺬﻛﺮ ﺇﻧﻤﺎ ﺃﻧﺖ'
             ' ﻣﺬﻛﺮ ﴿٢١﴾ ﻟﺴﺖ'
             ' ﻋﻠﻴﻬﻢ ﺑﻤﺼﻴﻄﺮ ﴿٢٢﴾'
             ' ﺇﻻ ﻣﻦ ﺗﻮﻟﻰ'
             ' ﻭﻛﻔﺮ ﴿٢٣﴾ ﻓﻴﻌﺬﺑﻪ'
             ' ﷲ ﺍﻟﻌﺬﺍﺏ'
             ' ﺍﻷﻛﺒﺮ ﴿٢٤﴾'),

            ('محمد رسول الله صلى الله عليه وسلم',
             'ﷴ ﷶ ﷲ ﷺ'),

            ('الله جل جلاله',
             'ﷲ ﷻ'),

            ('محمد رسول الله عليه صلى الله وسلم',
             'ﷴ ﷶ ﷲ ﷷ ﷹ ﷲ ﷸ'),
        )

    def test_reshaping(self):
        _reshaping_test(self)

if __name__ == '__main__':
    unittest.main()
