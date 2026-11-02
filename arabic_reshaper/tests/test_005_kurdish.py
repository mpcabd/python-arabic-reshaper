import unittest

import arabic_reshaper


class TestKurdishLamWithSmallV(unittest.TestCase):
    """U+06B5 has no Unicode presentation forms. Kurdish fonts draw its
    initial, medial and final forms from private-use code points
    U+E008, U+E009 and U+E007."""

    def setUp(self):
        self.reshaper = arabic_reshaper.ArabicReshaper(
            configuration={'language': 'Kurdish'}
        )

    def test_forms(self):
        cases = (
            # isolated
            ('ڵ', 'ڵ'),
            # initial, before meem
            ('ڵم', 'ﻢ'),
            # medial, between two meems
            ('مڵم', 'ﻣﻢ'),
            # final, after meem
            ('مڵ', 'ﻣ'),
        )
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(self.reshaper.reshape(text), expected)

    def test_words(self):
        cases = (
            # سڵاو (hello): medial
            ('سڵاو', 'ﺳﺎو'),
            # وڵات (country): initial, because waw does not join forward
            ('وڵات', 'وﺎت'),
            # گوڵ (flower): isolated, after waw
            ('گوڵ', 'ﮔﻮڵ'),
        )
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(self.reshaper.reshape(text), expected)


if __name__ == '__main__':
    unittest.main()
