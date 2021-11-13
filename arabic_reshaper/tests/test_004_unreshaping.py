from __future__ import unicode_literals
from __future__ import print_function

import unittest
import sys
import arabic_reshaper


def _unreshaping_test(test):
    for i, case in enumerate(test.cases):
        def t(): test.assertEqual(case[1], test.reshaper.unreshape(case[0]))
        if hasattr(test, 'subTest'):
            with test.subTest(i=i, case=case[0]):
                t()
        else:
            print('running test case %d' % i, file=sys.stderr)
            t()


class TestDefaultUnreshaping(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.default_reshaper
        self.cases = (
            # Reshaped text, Unreshaped text
            ('ﺍﻟﺴﻼﻡ ﻋﻠﻴﻜﻢ', 'السلام عليكم'),
            ('ﺍﻟﻠﻐﺔ ﺍﻟﻌﺮﺑﻴﺔ ﻫﻲ ﺃﻛﺜﺮ ﺍﻟﻠﻐﺎﺕ', 'اللغة العربية هي أكثر اللغات'),
            ('ﺗﺤﺪﺛﺎ ﻭﻧﻄﻘﺎ ﺿﻤﻦ ﻣﺠﻤﻮﻋﺔ', 'تحدثا ونطقا ضمن مجموعة'),
            ('ﺍﻟﻠﻐﺎﺕ ﺍﻟﺴﺎﻣﻴﺔ', 'اللغات السامية'),
            ('ﺍﻟﻌﺮﺑﻴﺔ ﻟﻐﺔ ﺭﺳﻤﻴﺔ ﻓﻲ', 'العربية لغة رسمية في'),
            ('ﻛﻞ ﺩﻭﻝ ﺍﻟﻮﻃﻦ ﺍﻟﻌﺮﺑﻲ', 'كل دول الوطن العربي'),
            ('ﺇﺿﺎﻓﺔ ﺇﻟﻰ ﻛﻮﻧﻬﺎ ﻟﻐﺔ', 'إضافة إلى كونها لغة'),
            ('ﺭﺳﻤﻴﺔ ﻓﻲ ﺗﺸﺎﺩ ﻭﺇﺭﻳﺘﺮﻳﺎ', 'رسمية في تشاد وإريتريا'),
            ('ﻭﺇﺳﺮﺍﺋﻴﻞ. ﻭﻫﻲ ﺇﺣﺪﻯ ﺍﻟﻠﻐﺎﺕ', 'وإسرائيل. وهي إحدى اللغات'),
            ('ﺍﻟﺮﺳﻤﻴﺔ ﺍﻟﺴﺖ ﻓﻲ ﻣﻨﻈﻤﺔ', 'الرسمية الست في منظمة'),
            ('ﺍﻷﻣﻢ ﺍﻟﻤﺘﺤﺪﺓ، ﻭﻳﺤﺘﻔﻞ', 'الأمم المتحدة، ويحتفل'),
            ('ﺑﺎﻟﻴﻮﻡ ﺍﻟﻌﺎﻟﻤﻲ ﻟﻠﻐﺔ ﺍﻟﻌﺮﺑﻴﺔ', 'باليوم العالمي للغة العربية'),
            ('ﻓﻲ 18 ﺩﻳﺴﻤﺒﺮ ﻛﺬﻛﺮﻯ ﺍﻋﺘﻤﺎﺩ', 'في 18 ديسمبر كذكرى اعتماد'),
            ('ﺍﻟﻌﺮﺑﻴﺔ ﺑﻴﻦ ﻟﻐﺎﺕ ﺍﻟﻌﻤﻞ ﻓﻲ', 'العربية بين لغات العمل في'),
            ('ﺍﻷﻣﻢ ﺍﻟﻤﺘﺤﺪﺓ.', 'الأمم المتحدة.'),
            ('ﺍﻵﻣﻢ ﺍﻟﻤﺘﺤﺪﺓ.', 'الآمم المتحدة.'),
            ('ﺍﺳﻢ ﻣﻦ amin ﺍﺳﺖ', 'اسم من amin است'),
        )

    def test_unreshaping(self):
        _unreshaping_test(self)


class TestUnreshapingWithHarakat(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.ArabicReshaper({
            'delete_harakat': False
        })
        self.cases = (
            # Reshaped text, Unreshaped text
            ('ﺍﻟﺴَﻼَْﻡٌ ﻋَﻠَﻴْﻜُﻢْ', 'السَلَاْمٌ عَلَيْكُمْ'),
            ('ﺍﻟﻠﻐﺔ ﺍﻟﻌﺮﺑﻴﺔ ﻫﻲ ﺃﻛﺜﺮ ﺍﻟﻠﻐﺎﺕ', 'اللغة العربية هي أكثر اللغات'),
            ('ﺗﺤﺪﺛﺎً ﻭﻧﻄﻘﺎً ﺿﻤﻦ ﻣﺠﻤﻮﻋﺔ', 'تحدثاً ونطقاً ضمن مجموعة'),
            ('ﺍﻟﻠﻐﺎﺕ ﺍﻟﺴﺎﻣﻴﺔ', 'اللغات السامية'),
            ('ﺍﻟﻌﺮﺑﻴﺔ ﻟﻐﺔ ﺭﺳﻤﻴﺔ ﻓﻲ', 'العربية لغة رسمية في'),
            ('ﻛﻞ ﺩﻭﻝ ﺍﻟﻮﻃﻦ ﺍﻟﻌﺮﺑﻲ', 'كل دول الوطن العربي'),
            ('ﺇﺿﺎﻓﺔ ﺇﻟﻰ ﻛﻮﻧﻬﺎ ﻟﻐﺔ', 'إضافة إلى كونها لغة'),
            ('ﺭﺳﻤﻴﺔ ﻓﻲ ﺗﺸﺎﺩ ﻭﺇﺭﻳﺘﺮﻳﺎ', 'رسمية في تشاد وإريتريا'),
            ('ﻭﺇﺳﺮﺍﺋﻴﻞ. ﻭﻫﻲ ﺇﺣﺪﻯ ﺍﻟﻠﻐﺎﺕ', 'وإسرائيل. وهي إحدى اللغات'),
            ('ﺍﻟﺮﺳﻤﻴﺔ ﺍﻟﺴﺖ ﻓﻲ ﻣﻨﻈﻤﺔ', 'الرسمية الست في منظمة'),
            ('ﺍﻷﻣﻢ ﺍﻟﻤﺘﺤﺪﺓ، ﻭﻳُﺤﺘﻔﻞ', 'الأمم المتحدة، ويُحتفل'),
            ('ﺑﺎﻟﻴﻮﻡ ﺍﻟﻌﺎﻟﻤﻲ ﻟﻠﻐﺔ ﺍﻟﻌﺮﺑﻴﺔ', 'باليوم العالمي للغة العربية'),
            ('ﻓﻲ 18 ﺩﻳﺴﻤﺒﺮ ﻛﺬﻛﺮﻯ ﺍﻋﺘﻤﺎﺩ', 'في 18 ديسمبر كذكرى اعتماد'),
            ('ﺍﻟﻌﺮﺑﻴﺔ ﺑﻴﻦ ﻟﻐﺎﺕ ﺍﻟﻌﻤﻞ ﻓﻲ', 'العربية بين لغات العمل في'),
            ('ﺍﻷﻣﻢ ﺍﻟﻤﺘﺤﺪﺓ.', 'الأمم المتحدة.'),
        )

    def test_unreshaping(self):
        _unreshaping_test(self)


class TestUnreshapingWithHarakatWithoutLigatures(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.ArabicReshaper({
            'delete_harakat': False,
            'support_ligatures': False
        })
        self.cases = (
            # Reshaped text, Unreshaped text
            ('ﺍﻟﺴَﻠَﺎْﻡٌ ﻋَﻠَﻴْﻜُﻢْ', 'السَلَاْمٌ عَلَيْكُمْ'),
            ('ﺍﻟﻠﻐﺔ ﺍﻟﻌﺮﺑﻴﺔ ﻫﻲ ﺃﻛﺜﺮ ﺍﻟﻠﻐﺎﺕ', 'اللغة العربية هي أكثر اللغات'),
            ('ﺗﺤﺪﺛﺎً ﻭﻧﻄﻘﺎً ﺿﻤﻦ ﻣﺠﻤﻮﻋﺔ', 'تحدثاً ونطقاً ضمن مجموعة'),
            ('ﺍﻟﻠﻐﺎﺕ ﺍﻟﺴﺎﻣﻴﺔ', 'اللغات السامية'),
            ('ﺍﻟﻌﺮﺑﻴﺔ ﻟﻐﺔ ﺭﺳﻤﻴﺔ ﻓﻲ', 'العربية لغة رسمية في'),
            ('ﻛﻞ ﺩﻭﻝ ﺍﻟﻮﻃﻦ ﺍﻟﻌﺮﺑﻲ', 'كل دول الوطن العربي'),
            ('ﺇﺿﺎﻓﺔ ﺇﻟﻰ ﻛﻮﻧﻬﺎ ﻟﻐﺔ', 'إضافة إلى كونها لغة'),
            ('ﺭﺳﻤﻴﺔ ﻓﻲ ﺗﺸﺎﺩ ﻭﺇﺭﻳﺘﺮﻳﺎ', 'رسمية في تشاد وإريتريا'),
            ('ﻭﺇﺳﺮﺍﺋﻴﻞ. ﻭﻫﻲ ﺇﺣﺪﻯ ﺍﻟﻠﻐﺎﺕ', 'وإسرائيل. وهي إحدى اللغات'),
            ('ﺍﻟﺮﺳﻤﻴﺔ ﺍﻟﺴﺖ ﻓﻲ ﻣﻨﻈﻤﺔ', 'الرسمية الست في منظمة'),
            ('ﺍﻟﺄﻣﻢ ﺍﻟﻤﺘﺤﺪﺓ، ﻭﻳُﺤﺘﻔﻞ', 'الأمم المتحدة، ويُحتفل'),
            ('ﺑﺎﻟﻴﻮﻡ ﺍﻟﻌﺎﻟﻤﻲ ﻟﻠﻐﺔ ﺍﻟﻌﺮﺑﻴﺔ', 'باليوم العالمي للغة العربية'),
            ('ﻓﻲ 18 ﺩﻳﺴﻤﺒﺮ ﻛﺬﻛﺮﻯ ﺍﻋﺘﻤﺎﺩ', 'في 18 ديسمبر كذكرى اعتماد'),
            ('ﺍﻟﻌﺮﺑﻴﺔ ﺑﻴﻦ ﻟﻐﺎﺕ ﺍﻟﻌﻤﻞ ﻓﻲ', 'العربية بين لغات العمل في'),
            ('ﺍﻟﺄﻣﻢ ﺍﻟﻤﺘﺤﺪﺓ.', 'الأمم المتحدة.'),
        )

    def test_unreshaping(self):
        _unreshaping_test(self)


class TestUnreshapingLigatures(unittest.TestCase):
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
            # Reshaped text, Unreshaped text
            (
             'ﺇﻧﻪ ﻣﻦ ﺳﻠﻴﻤﺎﻥ ﻭﺇﻧﻪ ﷽ ﴿٣٠﴾ '
             'ﺃﻻ ﺗﻌﻠﻮﺍ ﻋﻠﻲ ﻭﺃﺗﻮﻧﻲ ﻣﺴﻠﻤﻴﻦ ﴿٣١﴾',

             'إنه من سليمان وإنه بسم الله الرحمن الرحيم ﴿٣٠﴾ '
             'ألا تعلوا علي وأتوني مسلمين ﴿٣١﴾'
             ),
            (
                'ﻓﺬﻛﺮ ﺇﻧﻤﺎ ﺃﻧﺖ'
                ' ﻣﺬﻛﺮ ﴿٢١﴾ ﻟﺴﺖ'
                ' ﻋﻠﻴﻬﻢ ﺑﻤﺼﻴﻄﺮ ﴿٢٢﴾'
                ' ﺇﻻ ﻣﻦ ﺗﻮﻟﻰ'
                ' ﻭﻛﻔﺮ ﴿٢٣﴾ ﻓﻴﻌﺬﺑﻪ'
                ' ﷲ ﺍﻟﻌﺬﺍﺏ'
                ' ﺍﻷﻛﺒﺮ ﴿٢٤﴾',

                'فذكر إنما أنت'
                ' مذكر ﴿٢١﴾ لست'
                ' عليهم بمصيطر ﴿٢٢﴾'
                ' إلا من تولى'
                ' وكفر ﴿٢٣﴾ فيعذبه'
                ' الله العذاب'
                ' الأكبر ﴿٢٤﴾',
            ),

            (
                'ﷴ ﷶ ﷲ ﷺ',
                'محمد رسول الله صلى الله عليه وسلم',
            ),

            (
                'ﷲ ﷻ',
                'الله جل جلاله',
            ),

            (
                'ﷴ ﷶ ﷲ ﷷ ﷹ ﷲ ﷸ',
                'محمد رسول الله عليه صلى الله وسلم',
            ),
        )

    def test_unreshaping(self):
        _unreshaping_test(self)


if __name__ == '__main__':
    unittest.main()
