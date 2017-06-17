from __future__ import unicode_literals

import unittest
import arabic_reshaper


class TestDefaultConfiguration(unittest.TestCase):
    def setUp(self):
        self.reshaper = arabic_reshaper.ArabicReshaper()

    def boolean_check(self, boolean):
        self.assertIn(boolean, self.reshaper.configuration)
        self.assertIsNotNone(
            self.reshaper.configuration.getboolean(boolean)
        )

    def test_configuration_exists(self):
        self.assertIsNotNone(self.reshaper.configuration)

    def test_language(self):
        self.assertIn('language', self.reshaper.configuration)
        self.assertIsNotNone(self.reshaper.configuration['language'])
        self.assertTrue(self.reshaper.configuration['language'])

    def test_support_ligatures(self):
        self.boolean_check('support_ligatures')

    def test_delete_harakat(self):
        self.boolean_check('delete_harakat')

    def test_delete_tatweel(self):
        self.boolean_check('delete_tatweel')

    def test_ligatures(self):
        import arabic_reshaper.ligatures
        for ligature in arabic_reshaper.ligatures.LIGATURES:
            if hasattr(self, 'subTest'):
                with self.subTest(ligature=ligature[0]):
                    self.boolean_check(ligature[0])
            else:
                self.boolean_check(ligature[0])

if __name__ == '__main__':
    unittest.main()
