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


class TestKurdishFontForms(unittest.TestCase):
    """Forms checked against the Sarchia and Unikurd Web fonts, which draw
    them from these code points. See test_006_kurdish_font_glyphs.py."""

    def setUp(self):
        self.reshaper = arabic_reshaper.ArabicReshaper(
            configuration={'language': 'Kurdish'}
        )

    def check(self, cases):
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(self.reshaper.reshape(text), expected)

    def test_heh(self):
        self.check((
            ('\u0647', '\u0647'),
            ('\u0647\u0645', '\u06BE\uFEE2'),
            ('\u0645\u0647\u0645', '\uFEE3\uFBAB\uFEE2'),
            ('\u0645\u0647', '\uFEE3\uFEEA'),
            # هەولێر (Erbil): initial heh before ae
            ('\u0647\u06D5\u0648\u0644\u06CE\u0631',
             '\u06BE\uE000\u0648\uFEDF\uE006\uFEAE'),
        ))

    def test_isolated_hah_and_yeah(self):
        # Kurdish fonts have no glyph at U+FEA1, and U+E004 is the final
        # form of yeah, so the isolated forms use the base letters.
        self.check((
            ('\u062D', '\u062D'),
            ('\u06CE', '\u06CE'),
        ))

    def test_reh_with_small_v_below(self):
        self.check((
            ('\u0695', '\u0695'),
            ('\u0645\u0695', '\uFEE3\uE001'),
            # does not join the following letter
            ('\u0645\u0695\u0645', '\uFEE3\uE001\u0645'),
            # کوڕ (boy): isolated, after waw
            ('\u06A9\u0648\u0695', '\uFB90\uFEEE\u0695'),
        ))


if __name__ == '__main__':
    unittest.main()
