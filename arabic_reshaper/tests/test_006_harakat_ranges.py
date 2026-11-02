import unittest

import arabic_reshaper


class TestHarakatRanges(unittest.TestCase):
    def setUp(self):
        self.keep = arabic_reshaper.ArabicReshaper(
            configuration={'delete_harakat': False}
        )

    def test_extended_marks_do_not_break_joining(self):
        # Combining marks added in later Unicode versions must not split
        # the letters around them. U+FE91 and U+FE90 are initial and
        # final beh.
        for mark in ('\u0897', '\u089f', '\u08ca', '\u08d0', '\u08d3',
                     '\u08e1', '\u08e3', '\u08ff'):
            with self.subTest(mark='U+%04X' % ord(mark)):
                self.assertEqual(
                    self.keep.reshape('\u0628' + mark + '\u0628'),
                    '\ufe91' + mark + '\ufe90'
                )

    def test_disputed_end_of_ayah_is_not_a_haraka(self):
        # U+08E2 is a format character, so deleting harakat keeps it.
        self.assertIn('\u08e2', arabic_reshaper.reshape('\u0628\u08e2'))


if __name__ == '__main__':
    unittest.main()
