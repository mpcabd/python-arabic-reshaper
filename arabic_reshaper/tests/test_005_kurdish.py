import unittest

import arabic_reshaper


class TestKurdishLamWithSmallV(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.ArabicReshaper(
            configuration={'language': 'Kurdish'}
        )

    def test_forms(self):
        cases = (
            ('ڵ', 'ڵ'),
            ('ڵم', ''),
            ('مڵم', ''),
            ('مڵ', ''),
        )
        for text, form in cases:
            with self.subTest(text=text):
                self.assertIn(form, self.reshaper.reshape(text))


if __name__ == '__main__':
    unittest.main()
